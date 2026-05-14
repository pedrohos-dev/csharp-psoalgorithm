// ============================================================
// ResultPrinter.cs
// Exibe resultados e análise de convergência no console
// ============================================================

using System;
using System.Collections.Generic;

namespace PSO
{
    public static class ResultPrinter
    {
        /// <summary>
        /// Imprime o cabeçalho e o resultado final de uma execução.
        /// </summary>
        public static void PrintResult(PsoConfig config, PsoSolver solver, string label)
        {
            Console.WriteLine(new string('=', 60));
            Console.WriteLine($"  {label}");
            Console.WriteLine($"  c1={config.C1}  c2={config.C2}  Partículas={config.NumParticles}  Iterações={config.MaxIterations}");
            Console.WriteLine(new string('-', 60));
            Console.WriteLine($"  Melhor posição encontrada:");
            for (int d = 0; d < config.Dimensions; d++)
                Console.WriteLine($"    x[{d}] = {solver.GlobalBest[d]:F6}");
            Console.WriteLine($"  Fitness (f_Rastrigin) = {solver.GlobalBestFitness:F8}");
            Console.WriteLine($"  Ótimo global esperado : f(0,0) = 0");
            Console.WriteLine();
        }

        /// <summary>
        /// Imprime a evolução do fitness a cada 10 iterações.
        /// </summary>
        public static void PrintConvergenceTable(List<double> fitnessHistory)
        {
            Console.WriteLine("  Iteração | Melhor Fitness");
            Console.WriteLine("  " + new string('-', 30));
            for (int i = 0; i < fitnessHistory.Count; i++)
            {
                if ((i + 1) % 10 == 0 || i == 0)
                    Console.WriteLine($"  {i + 1,8} | {fitnessHistory[i],14:F8}");
            }
            Console.WriteLine();
        }

        /// <summary>
        /// Imprime tabela comparativa de todos os cenários.
        /// </summary>
        public static void PrintComparisonTable(List<(string Label, double C1, double C2, double BestFitness)> results)
        {
            Console.WriteLine(new string('=', 60));
            Console.WriteLine("  TABELA COMPARATIVA — EFEITO DE c1 e c2");
            Console.WriteLine(new string('-', 60));
            Console.WriteLine($"  {"Cenário",-20} {"c1",6} {"c2",6} {"Melhor Fitness",16}");
            Console.WriteLine("  " + new string('-', 50));
            foreach (var r in results)
                Console.WriteLine($"  {r.Label,-20} {r.C1,6:F1} {r.C2,6:F1} {r.BestFitness,16:F8}");
            Console.WriteLine(new string('=', 60));
        }
    }
}
