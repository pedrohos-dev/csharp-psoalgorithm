// ============================================================
// PsoConfig.cs
// Parâmetros de configuração do PSO
// ============================================================

namespace PSO
{
    public class PsoConfig
    {
        // --- Parâmetros do algoritmo ---
        public int    NumParticles   { get; set; } = 30;      // máx. 30 partículas (conforme enunciado)
        public int    Dimensions     { get; set; } = 2;       // n = 2 (conforme enunciado)
        public int    MaxIterations  { get; set; } = 100;     // critério de parada = 100 iterações
        public double LowerBound     { get; set; } = -5.12;   // domínio da Rastrigin
        public double UpperBound     { get; set; } =  5.12;

        // --- Coeficientes de aceleração ---
        public double C1 { get; set; } = 2.0;  // componente cognitivo
        public double C2 { get; set; } = 2.0;  // componente social

        // --- Inércia (redução linear) ---
        public double WMax { get; set; } = 0.9;
        public double WMin { get; set; } = 0.4;

        // --- Velocidade máxima ---
        public double VMax { get; set; } = 5.12;  // |domínio|

        // --- Semente para reprodução ---
        public int? Seed { get; set; } = null;   // null = aleatório
    }
}
