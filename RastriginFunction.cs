// ============================================================
// RastriginFunction.cs
// Função de Rastrigin (minimização)
// Mínimo global em f(0,...,0) = 0
// Domínio típico: [-5.12, 5.12]^n
// ============================================================

using System;

namespace PSO
{
    public static class RastriginFunction
    {
        private const double A = 10.0;

        /// <summary>
        /// Avalia a função de Rastrigin para um vetor de n dimensões.
        /// f(x) = A*n + sum[ x_i^2 - A*cos(2*pi*x_i) ]
        /// </summary>
        public static double Evaluate(double[] x)
        {
            int n = x.Length;
            double sum = A * n;
            for (int i = 0; i < n; i++)
            {
                sum += x[i] * x[i] - A * Math.Cos(2.0 * Math.PI * x[i]);
            }
            return sum;
        }
    }
}
