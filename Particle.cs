// ============================================================
// Particle.cs
// Representa uma partícula do enxame (PSO)
// ============================================================

namespace PSO
{
    public class Particle
    {
        public double[] Position { get; set; }
        public double[] Velocity { get; set; }
        public double[] PersonalBest { get; set; }
        public double PersonalBestFitness { get; set; }
        public int Dimensions { get; }

        public Particle(int dimensions, double lowerBound, double upperBound, Random rng)
        {
            Dimensions = dimensions;
            Position = new double[dimensions];
            Velocity = new double[dimensions];
            PersonalBest = new double[dimensions];

            for (int i = 0; i < dimensions; i++)
            {
                Position[i] = lowerBound + rng.NextDouble() * (upperBound - lowerBound);
                double vMax = (upperBound - lowerBound) / 2.0;
                Velocity[i] = -vMax + rng.NextDouble() * (2 * vMax);
                PersonalBest[i] = Position[i];
            }

            PersonalBestFitness = double.MaxValue;
        }
    }
}
