#include <stdio.h>
#include <unistd.h>
#include <fann.h>
#include <math.h>

int 
main(int argc, char **argv)
{
	fann_type *calc_out;
	unsigned int i, j;
	struct fann *ann;
	struct fann_train_data *data;
    float error = 0.0;

	if (argc < 3) 
	{
		fprintf(stderr, "Use: %s rede_FANN.net arquivoTeste\n", argv[0]); 
		exit(1);
	}

	printf("Abrindo a Rede `%s'\n", argv[1]);
	ann = fann_create_from_file(argv[1]);

	if (!ann)
	{
		fprintf(stderr, "Erro criando a RNA.\n"); 
		return (1); 
	}

	//fann_print_connections(ann);
	//fann_print_parameters(ann);

	printf("Testando a RNA.\n");

	data = fann_read_train_from_file(argv[2]);
	//fann_reset_MSE(ann);

	for(i = 0; i < fann_length_train_data(data); i++)
	{

		calc_out = fann_run(ann, data->input[i]);

		printf("Resultado: %f ", calc_out[0]);
		printf("Original: %f " , data->output[i][0]);
		printf("Erro: %f\n"    , (float) fann_abs(calc_out[0] - data->output[i][0]));
        error += (float) powf(fann_abs(calc_out[0] - data->output[i][0]),2);
	}

    //printf("Test MSE: %f\n", fann_get_MSE(ann));
    printf("Test:: Squared Error: %f Mean Squared Error: %f\n", error, error/(fann_length_train_data(data)-1));

	printf("Limpando memoria.\n");
	fann_destroy_train(data);
	fann_destroy(ann);

	return (0);
}
