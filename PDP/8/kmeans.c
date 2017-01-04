// #include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <unistd.h>

#define K           5
#define NUM_ITER    200

typedef struct Point{
    double x;
    double y;
    int    k;
} Point;

void print_point(Point point, char* msg) {
    printf("%s {x: %lf, y: %lf, k: %d}\n", msg, point.x, point.y, point.k);
}

Point* create_centroids() {
    srand(time(NULL));
    Point* centroids = (Point*) malloc(K * sizeof(Point));

    for (int i = 0; i < K; i++) {
        centroids[i].x = (double) rand() / (double) RAND_MAX;
        centroids[i].y = (double) rand() / (double) RAND_MAX;
        centroids[i].k = i;
    }

    return centroids;
}

double euclid_distance(Point p1, Point p2) {
    return sqrt( (p1.x - p2.x)*(p1.x - p2.x) + (p1.y - p2.y)*(p1.y - p2.y) );
}

Point update_centroid(Point* points, int number_points, int k) {
    Point centroid = {0.0, 0.0, k};

    int count = 0;
    for (int i = 0; i < number_points; i++) {
        if (points[i].k == k) {
            centroid.x += points[i].x;
            centroid.y += points[i].y;
            count++;
        }
    }

    if (count != 0) {
        centroid.x /= count;
        centroid.y /= count;
    }

    return centroid;
}

double closest_cluster(double* distance) {
    double min = distance[0];
    int    min_index = 0;

    for (int i = 0; i < K; i++) {
        if (distance[i] < min) {
            min = distance[i];
            min_index = i;
        }
    }

    return min_index;
}

void write_result(Point* centroids, Point* points, int number_points) {
    FILE* output = fopen("output.txt", "w");

    fprintf(output, "%d\n", K);
    for (int c = 0; c < K; c++) {
        fprintf(output, "%lf %lf %d\n", centroids[c].x, centroids[c].y, centroids[c].k);
    }
    for (int p = 0; p < number_points; p++) {
        fprintf(output, "%lf %lf %d\n", points[p].x, points[p].y, points[p].k);
    }

    fclose(output);
}


int main(int argc, char* argv[]) {

    /* Open file */
    FILE* input_data = fopen("input.txt", "r");
    if (input_data == NULL) {
        printf("File not found\n");
        fclose (input_data);
    }

    /* Read first number - number of points */
    int number_points;
    fscanf(input_data, "%d", &number_points);

    /* Create array of points */
    Point* points = (Point*) malloc(number_points * sizeof(Point));

    /* Fill array of points */
    for (int i = 0; i < number_points; i++) {
        fscanf(input_data, "%lf%lf", &points[i].x, &points[i].y);
        points[i].k = -1;
    }

    fclose(input_data);

    /* Create centroids (random) */
    Point* centroids = create_centroids();

    /* Create array with distances beetwen centroid and point */
    double* distance_to_centroid = (double*) malloc(K * sizeof(double));

    /* Main work */
    for (int iter = 0; iter < NUM_ITER; iter++) {
        for (int p = 0; p < number_points; p++) {
            for (int c = 0; c < K; c++) {
                distance_to_centroid[c] = euclid_distance(points[p], centroids[c]);
            }
            points[p].k = closest_cluster(distance_to_centroid);
        }
        for (int c = 0; c < K; c++) {
            centroids[c] = update_centroid(points, number_points, c);
        }
    }

    write_result(centroids, points, number_points);

    free(points);
    free(centroids);
    free(distance_to_centroid);

    return 0;
}