#include <stdio.h>
#include <unistd.h>
#include <fann.h>
#include <math.h>
#include <error.h>
#include <sys/stat.h>
#include <sys/types.h>

#include "Avaliador_Fann.h"

typedef struct {
	int qntCamadasOcultas, fcOculta, fcSaida,
	    neurOcultos, algAprend, epocasTreino;
	float learnRate, moment, decay;
}chromosome;

void checkArgs(int argc, char *argv[])
{
	if (argc != 10)
	{
		fprintf(stderr, "Use: %s\tQntCamadasOcultas  função-Cam.Oculta  função-Cam.Saída  Qnt-Neur.Ocultos\n"
                        "\t\t\tAlg.Aprendizado  LearningRate  Momentum  Decay  epocasTreinamento\n", argv[0]);
		exit(1);
	}
}

void buildChromosome(char *argv[], chromosome *chromo)
{
	chromo->qntCamadasOcultas  = atoi(argv[1]);
	chromo->fcOculta           = atoi(argv[2]);
	chromo->fcSaida            = atoi(argv[3]);
	chromo->neurOcultos        = atoi(argv[4]);
	chromo->algAprend          = atoi(argv[5]);
	chromo->learnRate          = atof(argv[6]);
	chromo->moment             = atof(argv[7]);
	chromo->decay              = atof(argv[8]);
	chromo->epocasTreino       = atof(argv[9]);
}

void checkDatasetFiles()
{
	if ( access( nomeArqTreino, F_OK ) == -1 )
	{
		error(2, 0, "Falha ao abrir o arquivo `%s'\n", nomeArqTreino);
	}

	if ( access( nomeArqValidacao, F_OK ) == -1 )
	{
		error(2, 0, "Falha ao abrir o arquivo `%s'\n", nomeArqValidacao);
	}
}

// If RNA File exists, then move it to another name
// Ex.: FILENAME.net -> FILENAME-0000.net
void checkIfRNAExists(char *fileName)
{
    char aux[1024], file[1024];
    int  count = 0;
    if ( access( fileName, F_OK ) == 0 )
    {
        while (fileName[count] != '\0')
        {
            file[count] = fileName[count];
            count++;
        }
        file[count-4] = '\0';
        for (count=0 ; count<9999; count++)
        {
            sprintf(aux, "%s-%04d.net", file, count);
            if ( access( aux, F_OK ) != 0 )
            {
                rename(fileName, aux);
                break;
            }
        }
    }
}

void saveANN(int argc, char* argv[], struct fann* ANN)
{
	int pos, i, aux;
	char ANN_filename[1024], ANN_full_filename[1024];
	mkdir(dirSaveRNAs, 0755);
	pos = 0;
	for (i = 1; i < argc; i++) {
		aux = 0;
		while (argv[i][aux] != '\0')
			ANN_filename[pos++] = argv[i][aux++];
		ANN_filename[pos++] = '_';
	}
	ANN_filename[pos - 1] = '\0';
	sprintf(ANN_full_filename, "%s/%s.net", dirSaveRNAs, ANN_filename);
    checkIfRNAExists(ANN_full_filename);
	fann_save(ANN, ANN_full_filename);
}

int main(int argc, char *argv[])
{
	struct fann_train_data *dadosTreino, *dadosTeste;
	struct fann *ANN;
	fann_type *ANN_Answers;

	int *layers, i, j, aux;
	chromosome chromo;

	float erro = 0.0;

	checkArgs(argc, argv);
	buildChromosome(argv, &chromo);

	checkDatasetFiles();

	dadosTreino = fann_read_train_from_file(nomeArqTreino);

	layers = (int *) calloc(2+chromo.qntCamadasOcultas, sizeof(int));
	layers[0] = qntNeuroniosEntrada;
	layers[2+chromo.qntCamadasOcultas-1] = qntNeuroniosSaida;
	aux = chromo.neurOcultos;
	for (i=1; i < 2+chromo.qntCamadasOcultas-1 ; i++)
	{
		layers[i] = aux;
		aux = aux/2;
	}

	// CRIANDO A RNA:
	ANN = fann_create_standard_array(2+chromo.qntCamadasOcultas, layers);

	// TREINO
	fann_set_learning_rate(ANN, chromo.learnRate);
	fann_set_learning_momentum(ANN, chromo.moment);

	fann_set_activation_function_hidden( ANN, chromo.fcOculta );
	fann_set_activation_function_output( ANN, chromo.fcSaida  );
	fann_set_training_algorithm(ANN, chromo.algAprend );

	if (fann_get_training_algorithm(ANN) == FANN_TRAIN_QUICKPROP)
		fann_set_quickprop_decay(ANN, chromo.decay);

	// Em python, o treino ficava entre um try.
	// Se desse erro, escrevia "Resultado: 999.0" e exit
	fann_train_on_data(ANN, dadosTreino, chromo.epocasTreino, 50, desiredError);

	fann_destroy_train(dadosTreino);

	// TESTES:
	dadosTeste  = fann_read_train_from_file( nomeArqValidacao);

	// Em python, o teste também ficava entre um try.
	// Se desse erro, escrevia "Resultado: 999.0" e exit
	for(i = 0; i < fann_length_train_data(dadosTeste); i++)
	{
		ANN_Answers = fann_run(ANN, dadosTeste->input[i]);
		if (ANN_Answers == NULL)
		{
			printf("Resultado: 999.0\n");
			exit(2);
		}

		for (j=0; j < qntNeuroniosSaida; j++)
			erro += (float) powf(fann_abs(ANN_Answers[j] - dadosTeste->output[i][j]), 2);
	}
	printf("Resultado: %f\n", erro/(fann_length_train_data(dadosTeste)-1));

	fann_destroy_train(dadosTeste);

	saveANN(argc, argv, ANN);

	fann_destroy(ANN);
}
