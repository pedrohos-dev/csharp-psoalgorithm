// ============================================================
// CsvExporter.cs
// Exporta histórico de fitness para análise externa (Excel/Python)
// ============================================================

using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;

namespace PSO
{
    public static class CsvExporter
    {
        /// <summary>
        /// Gera um arquivo CSV com o histórico de convergência de múltiplos cenários.
        /// </summary>
        public static void ExportConvergence(
            List<(string Label, List<double> History)> scenarios,
            string filePath = "convergence.csv")
        {
            using var sw = new StreamWriter(filePath);

            // Cabeçalho
            sw.Write("Iteracao");
            foreach (var s in scenarios)
                sw.Write($",{s.Label}");
            sw.WriteLine();

            int maxIter = 0;
            foreach (var s in scenarios)
                if (s.History.Count > maxIter) maxIter = s.History.Count;

            for (int i = 0; i < maxIter; i++)
            {
                sw.Write(i + 1);
                foreach (var s in scenarios)
                {
                    double val = i < s.History.Count ? s.History[i] : double.NaN;
                    sw.Write($",{val.ToString("F8", CultureInfo.InvariantCulture)}");
                }
                sw.WriteLine();
            }

            Console.WriteLine($"[CSV] Histórico de convergência exportado para: {filePath}");
        }

        /// <summary>
        /// Gera um arquivo CSV com as posições das partículas em cada iteração
        /// (útil para criar animações externas).
        /// </summary>
        public static void ExportPositions(
            List<double[][]> positionHistory,
            string filePath = "positions.csv")
        {
            using var sw = new StreamWriter(filePath);
            sw.WriteLine("Iteracao,Particula,X0,X1");

            for (int iter = 0; iter < positionHistory.Count; iter++)
            {
                var snapshot = positionHistory[iter];
                for (int p = 0; p < snapshot.Length; p++)
                {
                    sw.Write($"{iter + 1},{p + 1}");
                    foreach (double coord in snapshot[p])
                        sw.Write($",{coord.ToString("F6", CultureInfo.InvariantCulture)}");
                    sw.WriteLine();
                }
            }

            Console.WriteLine($"[CSV] Posições exportadas para: {filePath}");
        }
    }
}
