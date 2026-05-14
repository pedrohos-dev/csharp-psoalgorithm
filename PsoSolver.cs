// ============================================================
// PsoSolver.cs
// Núcleo do algoritmo PSO
// ============================================================

using System;
using System.Collections.Generic;

namespace PSO
{
    public class PsoSolver
    {
        // Configuração do enxame
        private readonly PsoConfig _config;
        private readonly Random _rng;

        // Estado do enxame
        private List<Particle> _swarm;
        private double[] _globalBest;
        private double _globalBestFitness;

        // Histórico para análise
        public List<double> FitnessHistory { get; } = new List<double>();
        public List<double[][]> PositionHistory { get; } = new List<double[][]>();

        public double[] GlobalBest => _globalBest;
        public double GlobalBestFitness => _globalBestFitness;

        public PsoSolver(PsoConfig config)
        {
            _config = config;
            _rng = new Random(config.Seed ?? Environment.TickCount);
        }

        /// <summary>
        /// Executa o PSO e retorna o melhor fitness encontrado.
        /// </summary>
        public double Run()
        {
            Initialize();

            for (int iter = 0; iter < _config.MaxIterations; iter++)
            {
                double w = ComputeInertia(iter);

                foreach (var particle in _swarm)
                {
                    UpdateVelocityAndPosition(particle, w);
                    ClampPosition(particle);

                    double fitness = RastriginFunction.Evaluate(particle.Position);

                    // Atualiza personal best
                    if (fitness < particle.PersonalBestFitness)
                    {
                        particle.PersonalBestFitness = fitness;
                        Array.Copy(particle.Position, particle.PersonalBest, _config.Dimensions);
                    }

                    // Atualiza global best
                    if (fitness < _globalBestFitness)
                    {
                        _globalBestFitness = fitness;
                        Array.Copy(particle.Position, _globalBest, _config.Dimensions);
                    }
                }

                FitnessHistory.Add(_globalBestFitness);

                // Salva snapshot das posições para visualização
                var snapshot = new double[_swarm.Count][];
                for (int i = 0; i < _swarm.Count; i++)
                {
                    snapshot[i] = (double[])_swarm[i].Position.Clone();
                }
                PositionHistory.Add(snapshot);
            }

            return _globalBestFitness;
        }

        // --------------------------------------------------------
        // Inicialização
        // --------------------------------------------------------
        private void Initialize()
        {
            _swarm = new List<Particle>(_config.NumParticles);
            _globalBest = new double[_config.Dimensions];
            _globalBestFitness = double.MaxValue;
            FitnessHistory.Clear();
            PositionHistory.Clear();

            for (int i = 0; i < _config.NumParticles; i++)
            {
                var p = new Particle(_config.Dimensions, _config.LowerBound, _config.UpperBound, _rng);
                double fitness = RastriginFunction.Evaluate(p.Position);
                p.PersonalBestFitness = fitness;
                Array.Copy(p.Position, p.PersonalBest, _config.Dimensions);

                if (fitness < _globalBestFitness)
                {
                    _globalBestFitness = fitness;
                    Array.Copy(p.Position, _globalBest, _config.Dimensions);
                }

                _swarm.Add(p);
            }
        }

        // --------------------------------------------------------
        // Atualização de velocidade e posição
        // --------------------------------------------------------
        private void UpdateVelocityAndPosition(Particle p, double w)
        {
            for (int d = 0; d < _config.Dimensions; d++)
            {
                double r1 = _rng.NextDouble();
                double r2 = _rng.NextDouble();

                double cognitive = _config.C1 * r1 * (p.PersonalBest[d] - p.Position[d]);
                double social    = _config.C2 * r2 * (_globalBest[d]     - p.Position[d]);

                p.Velocity[d] = w * p.Velocity[d] + cognitive + social;

                // Clamp de velocidade
                p.Velocity[d] = Math.Max(-_config.VMax, Math.Min(_config.VMax, p.Velocity[d]));

                p.Position[d] += p.Velocity[d];
            }
        }

        // --------------------------------------------------------
        // Mantém a partícula dentro dos limites
        // --------------------------------------------------------
        private void ClampPosition(Particle p)
        {
            for (int d = 0; d < _config.Dimensions; d++)
            {
                if (p.Position[d] < _config.LowerBound)
                {
                    p.Position[d] = _config.LowerBound;
                    p.Velocity[d] *= -1; // rebate
                }
                else if (p.Position[d] > _config.UpperBound)
                {
                    p.Position[d] = _config.UpperBound;
                    p.Velocity[d] *= -1;
                }
            }
        }

        // --------------------------------------------------------
        // Inércia com redução linear (Shi & Eberhart, 1998)
        // w(k) = wMax - k * (wMax - wMin) / kMax
        // --------------------------------------------------------
        private double ComputeInertia(int currentIter)
        {
            return _config.WMax - currentIter * (_config.WMax - _config.WMin) / _config.MaxIterations;
        }
    }
}
