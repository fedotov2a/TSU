#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <unistd.h>
#include <float.h>

#define MAX_ITER  700

/* Матрица расстояний */
double* matrix_distances;

/* Количество городов */
int number_cities;

/* Счетчик итераций */
int iter = 0;

/* Массив с минимальными расстояниями от каждого потока */
double* min_distances;

/* Массив последовательностей посещения городов */
int* min_paths;

int* generate_path(int rank) {
    int* cities = (int*) malloc( number_cities * sizeof(int) );
    cities[0] = -1;

    for (int i = 1; i < number_cities; i++) {
        cities[i] = i;
    }

    int* path = (int*) malloc( (number_cities + 1) * sizeof(int) );
    path[0] = 0;
    path[number_cities] = 0;

    int k = 1;

    /* Генерируем случайный путь, исключая повторяющиеся значения */
    while(1) {
        int g = 1 + rand() % (number_cities - 1);
        if (cities[g] != -1) {
            path[k] = g;
            cities[g] = -1;
            k++;
        }

        if (k == number_cities) {
            break;
        }
    }

    free(cities);
    return path;
}

double which_distance(int* path) {
    double distance = 0.0;

    /* Подсчет расстояния в сгенерированном пути */
    for (int i = 0; i < number_cities; i++) {
        distance += matrix_distances[path[i] * number_cities + path[i+1]];
    }

    return distance;
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank;
    int size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0) {
        /* Open and read file */
        FILE* input_data = fopen("matrix_distances.txt", "r");
        if (input_data == NULL) {
            printf("File not found\n");
            fclose (input_data);
        }

        fscanf(input_data, "%d", &number_cities);
        matrix_distances = (double*) malloc(number_cities * number_cities * sizeof(double));

        for (int c = 0; c < number_cities * number_cities; c++) {
            fscanf(input_data, "%lf", &matrix_distances[c]);
        }

        fclose(input_data);

    }

    MPI_Barrier(MPI_COMM_WORLD);

    /* Из нулевого потока отправить всем остальным количество городов */
    MPI_Bcast(&number_cities, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank != 0) {
        matrix_distances = (double*) malloc(number_cities * number_cities * sizeof(double));
    }

    /* Из нулевого потока отправить всем остальным массив расстояний */
    MPI_Bcast(matrix_distances, number_cities * number_cities, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);

    double min_distance = DBL_MAX;
    int* min_path = (int*) malloc((number_cities + 1) * sizeof(int));

    int* path;
    double distance;

    usleep( (rank + number_cities) * MAX_ITER * number_cities );
    srand((unsigned)time(NULL) + (rank + 1) * number_cities);

    /* Main work */
    while (iter < MAX_ITER) {
        path = generate_path(rank);
        distance = which_distance(path);

        if ( distance < min_distance ) {
            min_distance = distance;

            for (int i = 0; i < number_cities + 1; i++) {
                min_path[i] = path[i];
            }
        }

        iter++;
    }
    MPI_Barrier(MPI_COMM_WORLD);

    if (rank == 0) {
        min_distances = (double*) malloc(size * sizeof(double));
        min_paths = (int*) malloc(size * (number_cities + 1) * sizeof(int));
    }

    // Собрать все минимальные дистанции со всех потоков
    MPI_Gather(&min_distance, 1, MPI_DOUBLE, min_distances, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Gather(min_path, number_cities + 1, MPI_INT, min_paths, number_cities + 1, MPI_INT, 0, MPI_COMM_WORLD);

    /* Собрали все данные со всех потоков в нулевом, теперь ищем минимальный путь среди минимальных */
    if (rank == 0) {
        // for (int i = 0; i < size; i++) {
        //     printf("%lf ", min_distances[i]);
        // }
        // printf("\n");
        
        // for (int i = 0; i < size * (number_cities + 1); i++) {
        //     if (i % (number_cities + 1) == 0) {
        //         printf("\n");
        //     }
        //     printf("%d ", min_paths[i]);
        // }

        double min = min_distances[0];
        int min_index = 0;
        for (int i = 1; i < size; i++) {
            if (min_distances[i] < min) {
                min = min_distances[i];
                min_index = i;
            }
        }

        FILE* result = fopen("min_path.txt", "w");

        fprintf(result, "%lf\n", min);
        printf("\nMin distance: %lf\n", min);
        printf("Min path: ");

        for (int i = min_index * (number_cities + 1), k = 0; k < number_cities + 1; i++, k++) {
            printf("%d ", min_paths[i]);
            fprintf(result, "%d ", min_paths[i]);
        }
        printf("\n");

        fclose(result);

        int* pp = (int*) malloc( (number_cities + 1) * sizeof(int) );
        pp[0] = 0;
        pp[number_cities] = 0;
        for (int i = 1; i < number_cities; i++) {
            pp[i] = i;
        }
        double pp_p = which_distance(pp);
        printf("\n%lf\n", pp_p);
    }


    MPI_Finalize();
    return 0;
}
