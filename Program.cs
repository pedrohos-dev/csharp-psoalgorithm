// ============================================================
// Program.cs  (CORRIGIDO)
// Ponto de entrada — executa todos os cenários do enunciado
// ============================================================

using System;
using System.Collections.Generic;

namespace PSO
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;

            // Cenários de c1 e c2 exigidos pelo enunciado
            // "key" é usado como sufixo limpo nos nomes de arquivo
            var scenarios = new List<(string key, double c1, double c2)>
            {
                ("c1_0_c2_1",   0.0, 1.0),
                ("c1_1_c2_0",   1.0, 0.0),
                ("c1_1_c2_1",   1.0, 1.0),
                ("c1_1_c2_01",  1.0, 0.1),
                ("c1_2_c2_2",   2.0, 2.0),
                ("c1_4_c2_4",   4.0, 4.0),
            };

            var comparison   = new List<(string Label, double C1, double C2, double BestFitness)>();
            var convergences = new List<(string Label, List<double> History)>();

            foreach (var (key, c1, c2) in scenarios)
            {
                string label = $"c1={c1} / c2={c2}";

                var config = new PsoConfig
                {
                    NumParticles  = 30,
                    Dimensions    = 2,
                    MaxIterations = 100,
                    LowerBound    = -5.12,
                    UpperBound    =  5.12,
                    C1            = c1,
                    C2            = c2,
                    WMax          = 0.9,
                    WMin          = 0.4,
                    VMax          = 5.12,
                    Seed          = 42
                };

                var solver = new PsoSolver(config);
                solver.Run();

                ResultPrinter.PrintResult(config, solver, label);
                ResultPrinter.PrintConvergenceTable(solver.FitnessHistory);

                comparison.Add((label, c1, c2, solver.GlobalBestFitness));
                convergences.Add((key, new List<double>(solver.FitnessHistory)));

                // Nome de arquivo simples, sem caracteres especiais
                string posFile = $"positions_{key}.csv";
                CsvExporter.ExportPositions(solver.PositionHistory, posFile);
            }

            ResultPrinter.PrintComparisonTable(comparison);
            CsvExporter.ExportConvergence(convergences, "convergence_all.csv");

            Console.WriteLine("\nArquivos CSV gerados na pasta do executável.");
            Console.WriteLine("Pressione qualquer tecla para sair...");
            Console.ReadKey();
        }
    }
}
