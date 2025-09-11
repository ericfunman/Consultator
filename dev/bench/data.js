window.BENCHMARK_DATA = {
  "lastUpdate": 1757600208395,
  "repoUrl": "https://github.com/ericfunman/Consultator",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "lapinae@gmail.com",
            "name": "Eric Funman",
            "username": "ericfunman"
          },
          "committer": {
            "email": "lapinae@gmail.com",
            "name": "Eric Funman",
            "username": "ericfunman"
          },
          "distinct": true,
          "id": "927ac20ac1038609f9391027cd73136b6595de62",
          "message": "fix: Configurer l'identité Git pour les benchmarks\n\n- Ajouter configuration Git avec nom 'Eric Lapina' et email 'lapinae@gmail.com'\n- Résoudre l'erreur 'empty ident name not allowed'\n- Permettre aux actions benchmark de faire des commits sur gh-pages",
          "timestamp": "2025-09-11T16:11:44+02:00",
          "tree_id": "50f6f9d1e40693bd145e8755e356747a323bc13c",
          "url": "https://github.com/ericfunman/Consultator/commit/927ac20ac1038609f9391027cd73136b6595de62"
        },
        "date": 1757600208096,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2952215597116,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013612782542923455",
            "extra": "mean: 1.0623659581985505 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 288840.7326208913,
            "unit": "iter/sec",
            "range": "stddev: 5.27405729286588e-7",
            "extra": "mean: 3.462115578111755 usec\nrounds: 111907"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156731.62513165615,
            "unit": "iter/sec",
            "range": "stddev: 8.504724578916815e-7",
            "extra": "mean: 6.380333255397497 usec\nrounds: 106987"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33303.345209622814,
            "unit": "iter/sec",
            "range": "stddev: 0.000004664842620661597",
            "extra": "mean: 30.02701361396739 usec\nrounds: 18951"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.6449312262293,
            "unit": "iter/sec",
            "range": "stddev: 0.000015701546810419726",
            "extra": "mean: 5.085307786802572 msec\nrounds: 197"
          }
        ]
      }
    ]
  }
}