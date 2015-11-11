import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import static java.lang.Math.sqrt;
import java.util.Random;
import java.util.Scanner;

public class Recommender {

    public static void main(String[] args) {
        String f1 = args[0];
        String f2 = args[1];
        int r = Integer.parseInt(args[2]);
        double mu = Double.parseDouble(args[3]); 
        double lamda = Double.parseDouble(args[4]);
        
        int[][] A = readfile(f1);
        int m = 1000, n = 2069;
        double[][] U_initial = randomize(m, r, r);
        double[][] V_initial = randomize(r, n, r);
        double[][] U_final = new double[m][r];
        double[][] V_final = new double[r][n];
        int[][] M = create_M(m, n, A);
        update_UV(M, U_final, V_final, U_initial, V_initial, mu, lamda);
        double[][] UV_final = matrix_multiply(U_final, V_final);
        double[][] UV_round = round_matrix(UV_final);
        //double[][] M_double = convert_matrix2double(M);
        //print_all(UV_final, UV_round, M_double);
        fill_rating_result(f2,UV_round);
    }
    
    public static void fill_rating_result(String f2, double[][] UV_round) {
        int[][] B = readfile(f2);
        String f3 = "results.csv";
        try (PrintWriter writer = new PrintWriter(f3)) {
            for (int[] B1 : B) {
                for (int j = 0; j < B[0].length; j++) {
                    writer.print(B1[j]);
                    writer.print(",");
                }
                writer.print((int) UV_round[B1[0] - 1][B1[1] - 1]);
                writer.println();
            }
            writer.close();
        } catch (FileNotFoundException ex) {
            System.out.println("File not found.");
        }
    }

    public static void print_all(double[][] UV_final, double[][] UV_round, double[][] M_double) {
        write_matrix(UV_round, "predicted_rating_rounded.csv");
        write_matrix(UV_final, "predicted_rating.csv");
        write_matrix(M_double, "true_rating.csv");
    }

    public static void write_matrix(double[][] A, String f1) {
        try (PrintWriter writer = new PrintWriter(f1)) {
            for (double[] A1 : A) {
                for (int j = 0; j < A[0].length; j++) {
                    writer.printf("%.4f", A1[j]);
                    if (j != A[0].length - 1) {
                        writer.print(",");
                    }
                }
                writer.println();
            }
            writer.close();
        } catch (FileNotFoundException ex) {
            System.out.println("File not found.");
        }
    }

    public static int[][] readfile(String f1) {
        File fp = new File(f1);
        int LINES = data_length(f1);
        int COLUMN = data_width(f1);
        int[][] A = new int[LINES][COLUMN];
        try (Scanner input = new Scanner(fp)) {
            for (int i = 0; i < LINES; i++) {
                String data = input.next();
                String[] val = data.split(",");
                for (int j = 0; j < COLUMN; j++) {
                    A[i][j] = Integer.parseInt(val[j]);
                }
            }
            input.close();
        } catch (FileNotFoundException ex) {
            System.out.println("File not found.");
        }
        return A;
    }

    public static int data_length(String f1) {
        int LINES = 0;
        File fp = new File(f1);
        try (Scanner input = new Scanner(fp)) {
            while (input.hasNext()) {
                LINES++;
                input.next();
            }
            input.close();
        } catch (FileNotFoundException ex) {
            System.out.println("File not found.");
        }
        return LINES;
    }

    public static int data_width(String f1) {
        int COLUMN = 0;
        File fp = new File(f1);
        try (Scanner input = new Scanner(fp)) {
            String data = input.next();
            String[] val = data.split(",");
            COLUMN = val.length;
            input.close();
        } catch (FileNotFoundException ex) {
            System.out.println("File not found.");
        }
        return COLUMN;
    }

    public static double[][] randomize(int m, int n, int rr) {
        double[][] R = new double[m][n];
        Random r = new Random();
        double alpha;
        if (rr == 5) 
            alpha = 0.5;
        else if (rr == 3)
            alpha = 0.3;
        else if (rr == 1)
            alpha = 2.5;
        else alpha = sqrt(5/rr);
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                R[i][j] = alpha*r.nextDouble();
            }
        }
        return R;
    }

    public static void update_UV(int[][] M, double[][] U_final, double[][] V_final, double[][] U_initial,
            double[][] V_initial, double mu, double lamda) {
        int max_iteration = 50;
        double min_RMSE = 0.26;
        if (mu == 0.00001)
            min_RMSE = 0.20;
        double RMSE = 1E6;
        double[][] UV_initial = matrix_multiply(U_initial, V_initial);
        double E;
        int ite = 0;
        while (ite < max_iteration && RMSE > min_RMSE) {
            update_U(M, UV_initial, U_final, U_initial, V_initial, mu, lamda);
            update_V(M, UV_initial, V_final, U_initial, V_initial, mu, lamda);
            double[][] UV_final = matrix_multiply(U_final, V_final);
            E = find_E(M, UV_final, U_final, V_final, lamda);
            double E_evaluate = find_E(M, UV_final, U_final, V_final, 0);
            RMSE = sqrt(E_evaluate/(M.length*M[0].length));
            copy_array(U_final, U_initial);
            copy_array(V_final, V_initial);
            copy_array(UV_final, UV_initial);
            ite++;
            //System.out.println("Reconstruction error at " + ite + " step: " + E);
            System.out.println("RMSE of Reconstruction at " + ite + "th step: " + RMSE);
        }
        System.out.println("Number of iterations: " + ite);
    }

    public static void update_U(int[][] M, double[][] UV_initial, double[][] U_final, double[][] U_initial, double[][] V_initial,
            double mu, double lamda) {
        for (int u = 0; u < U_initial.length; u++) {
            for (int k = 0; k < U_initial[0].length; k++) {
                double dU = find_dU(u, k, M, UV_initial, U_initial, V_initial, lamda);
                U_final[u][k] = U_initial[u][k] - mu*dU;
            }
        }
    }
    
    public static void update_V(int[][] M, double[][] UV_initial, double[][] V_final, double[][] U_initial, double[][] V_initial,
            double mu, double lamda) {
        for (int k = 0; k < V_initial.length; k++) {
            for (int i = 0; i < V_initial[0].length; i++) {
                double dV = find_dV(k, i, M, UV_initial, U_initial, V_initial, lamda);
                V_final[k][i] = V_initial[k][i] - mu*dV;
            }
        }
    }

    public static double find_dU(int u, int k, int[][] M, double[][] UV_initial,
            double[][] U_initial, double[][] V_initial, double lamda) {
        double term = 0;
        for (int i = 0; i < M[0].length; i++) {
            term += 2*(M[u][i] - UV_initial[u][i]) * (-V_initial[k][i]);
        }
        double du = term + 2 * lamda * U_initial[u][k];
        return du;
    }

    public static double find_dV(int k, int i, int[][] M, double[][] UV_initial,
            double[][] U_initial, double[][] V_initial, double lamda) {
        double term = 0;
        for (int u = 0; u < M.length; u++) {
            term += 2 * (M[u][i] - UV_initial[u][i]) * (-U_initial[u][k]);
        }
        double dV = term + 2 * lamda * V_initial[k][i];
        return dV;
    }

    public static double find_E(int[][] M, double[][] UV, double[][] U, double[][] V, double lamda) {
        double[][] M_double = convert_matrix2double(M);
        double[][] M_UV_diff = subtract_matrix(M_double, UV);
        double E = sum_of_square(M_UV_diff);
        E += lamda * (sum_of_square(U) + sum_of_square(V));
        return E;
    }

    public static double[][] convert_matrix2double(int[][] M) {
        double[][] M_double = new double[M.length][M[0].length];
        for (int i = 0; i < M.length; i++) {
            for (int j = 0; j < M[0].length; j++) {
                M_double[i][j] = (double) M[i][j];
            }
        }
        return M_double;
    }
    
    public static double[][] round_matrix(double[][] M) {
        double[][] M_round = new double[M.length][M[0].length];
        for (int i = 0; i < M.length; i++) {
            for (int j = 0; j < M[0].length; j++) {
                M_round[i][j] =  Math.round(M[i][j]);
            }
        }
        return M_round;
    }

    public static double[][] subtract_matrix(double[][] A, double[][] B) {
        double[][] C = new double[A.length][A[0].length];
        for (int i = 0; i < A.length; i++) {
            for (int j = 0; j < A[0].length; j++) {
                C[i][j] = A[i][j] - B[i][j];
            }
        }
        return C;
    }

    public static double sum_of_square(double[][] A) {
        double sos = 0;
        for (double[] A1 : A) {
            for (int j = 0; j < A[0].length; j++) {
                sos += A1[j] * A1[j];
            }
        }
        return sos;
    }

    public static void copy_array(double[][] A, double[][] B) { //Copy array A into B
        for (int i = 0; i < A.length; i++) {
            System.arraycopy(A[i], 0, B[i], 0, A[0].length);
        }
    }

    public static double[][] matrix_multiply(double[][] A, double[][] B) {
        int m = A.length, n = A[0].length, p = B[0].length;
        double[][] C = new double[m][p];
        double sum;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < p; j++) {
                sum = 0;
                for (int k = 0; k < n; k++) {
                    sum += A[i][k] * B[k][j];
                }
                C[i][j] = sum;
            }
        }
        return C;
    }

    public static int[][] create_M(int m, int n, int[][] A) {
        int[][] M = zero(m, n);
        fill_ratings(M, A);
        fill_missing_ratings(M);
        return M;
    }

    public static int[][] zero(int m, int n) {
        int[][] M = new int[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                M[i][j] = 0;
            }
        }
        return M;
    }

    public static void fill_ratings(int[][] M, int[][] A) {
        int user_ID, item_ID;
        for (int[] A1 : A) {
            user_ID = A1[0] - 1;
            item_ID = A1[1] - 1;
            M[user_ID][item_ID] = A1[2];
        }
    }

    public static void fill_missing_ratings(int[][] M) {
        int[] avg = find_avg_ratings(M);
        for (int i = 0; i < M.length; i++) {
            for (int j = 0; j < M[0].length; j++) {
                if (M[i][j] == 0) {
                    M[i][j] = avg[i];
                }
            }
        }
    }

    public static int[] find_avg_ratings(int[][] M) {
        int[] avg = new int[M.length];
        for (int i = 0; i < M.length; i++) {
            double sum = 0;
            int count = 0;
            for (int j = 0; j < M[0].length; j++) {
                if (M[i][j] != 0) {
                    count++;
                    sum += M[i][j];
                }
            }
            int row_avg = (int) Math.round(sum/count);
            avg[i] = row_avg;
        }
        return avg;
    }
}
