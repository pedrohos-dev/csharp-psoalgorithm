# PSO Algorithm Visualization (C# + Python)

Implementação do algoritmo PSO (Particle Swarm Optimization) com visualização 2D da função de Rastrigin.

## 📁 Estrutura de Pastas

```
csharp-psoalgorithm/
├── particle-positions-csv/          # 📊 Posições das partículas (iteração × partícula)
├── particle-plots-png/              # 🖼️  Contour plots estáticos (4 snapshots)
├── videos/                          # 🎥 Animações MP4/GIF da evolução do enxame
├── convergence-csv/                 # 📈 Histórico de fitness de cada cenário
├── bin/ obj/                        # 🔧 Artefatos de build .NET
├── Program.cs                       # 🚀 Entrada do PSO solver
├── PsoSolver.cs                     # 🧬 Núcleo do algoritmo PSO
├── PsoConfig.cs                     # ⚙️  Configurações (c1, c2, w, etc)
├── Particle.cs                      # 🔵 Estrutura de partícula
├── RastriginFunction.cs             # 📐 Função de otimização
├── CsvExporter.cs                   # 💾 Exportação de dados
├── ResultPrinter.cs                 # 🖨️  Impressão de resultados
├── plot_contour.py                  # 📊 Gerador de gráficos estáticos
├── generate_video.py                # 🎬 Gerador de vídeos/GIFs
└── pso-csharp.sln                   # 📋 Solução Visual Studio
```

## 🚀 Como Executar

### 1. Gerar dados PSO
```bash
dotnet run
```
Isso executa 100 iterações com diferentes combinações de c1/c2 e salva:
- `particle-positions-csv/positions_*.csv` (posições das 30 partículas)
- `convergence-csv/convergence_all.csv` (histórico de fitness)

### 2. Gerar gráficos estáticos
```bash
python plot_contour.py
```
Gera contour plot com 4 snapshots em `particle-plots-png/`

### 3. Gerar animações
```bash
python generate_video.py
```
Cria MP4 (requer ffmpeg) ou GIF em `videos/`

## 📊 Cenários Testados

- `c1_0_c2_1` - Social apenas
- `c1_1_c2_0` - Cognitivo apenas
- `c1_1_c2_1` - Balanceado
- `c1_1_c2_01` - Social dominante
- `c1_2_c2_2` - Agressivo
- `c1_4_c2_4` - Super agressivo

## 🐍 Dependências Python

```bash
pip install matplotlib numpy pandas
ffmpeg  # para gerar MP4 (opcional; GIF usa PIL)
```

## 📌 Notas

- Função de teste: **Rastrigin** (n=2, domínio [-5.12, 5.12]²)
- Ótimo global: **(0, 0)** com f(0,0) = 0
- Partículas: 30
- Iterações: 100
- Vmax: 5.12, Inércia linear: [0.9, 0.4]

## 📝 Formato dos CSVs

**positions_*.csv:**
```
Iteracao,Particula,X0,X1
1,1,-1.940690,-3.521113
1,2,-5.120000,2.333534
...
```

**convergence_all.csv:**
```
Iteracao,c1_0_c2_1,c1_1_c2_0,c1_1_c2_1,...
1,8.54855662,8.54855662,8.54855662,...
2,3.41201860,8.54855662,6.07755266,...
...
```
