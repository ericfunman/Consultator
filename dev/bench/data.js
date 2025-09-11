window.BENCHMARK_DATA = {
  "lastUpdate": 1757603255412,
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
      },
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
          "id": "f492c4176eb8beb114c2c580ec10473d6c82acee",
          "message": "fix: Tests de régression exécutent maintenant TOUS les tests\n\n- Suppression du filtre -m regression pour exécuter tous les tests\n- Augmentation du timeout à 300s pour gérer tous les tests\n- Modification des messages pour refléter l'exécution complète\n- Le job regression-tests exécute maintenant les 486 tests complets",
          "timestamp": "2025-09-11T16:20:09+02:00",
          "tree_id": "336d2c70865cb9c6a8ef874cc9a6c5175247291c",
          "url": "https://github.com/ericfunman/Consultator/commit/f492c4176eb8beb114c2c580ec10473d6c82acee"
        },
        "date": 1757600664096,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4736788511242,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021058894856563945",
            "extra": "mean: 1.0621645856528834 msec\nrounds: 934"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 286684.9733795575,
            "unit": "iter/sec",
            "range": "stddev: 5.277385751665898e-7",
            "extra": "mean: 3.488149337621707 usec\nrounds: 115115"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156879.51856611742,
            "unit": "iter/sec",
            "range": "stddev: 8.28584402529986e-7",
            "extra": "mean: 6.37431838865917 usec\nrounds: 75166"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33005.05219970383,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017461631944543692",
            "extra": "mean: 30.298391711344525 usec\nrounds: 21789"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.47012890349936,
            "unit": "iter/sec",
            "range": "stddev: 0.000015512782819636255",
            "extra": "mean: 5.0898322588833445 msec\nrounds: 197"
          }
        ]
      },
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
          "id": "e4248b8d6ae41f1ad75786cef9d5ad5101f81a18",
          "message": "fix: Recréer complètement le workflow SonarQube avec configuration simplifiée",
          "timestamp": "2025-09-11T16:49:42+02:00",
          "tree_id": "929d56d640c3ab39cebfc8c61b2e15c79627f576",
          "url": "https://github.com/ericfunman/Consultator/commit/e4248b8d6ae41f1ad75786cef9d5ad5101f81a18"
        },
        "date": 1757602473055,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4201653748514,
            "unit": "iter/sec",
            "range": "stddev: 0.000001916313608807815",
            "extra": "mean: 1.0622249626465388 msec\nrounds: 937"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289656.00634363265,
            "unit": "iter/sec",
            "range": "stddev: 5.350540068969868e-7",
            "extra": "mean: 3.4523710128546505 usec\nrounds: 114996"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159624.6439930409,
            "unit": "iter/sec",
            "range": "stddev: 8.141304855149487e-7",
            "extra": "mean: 6.26469682240041 usec\nrounds: 72855"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34438.547519470325,
            "unit": "iter/sec",
            "range": "stddev: 0.000001785273529693676",
            "extra": "mean: 29.037229268587346 usec\nrounds: 21224"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.5139349657299,
            "unit": "iter/sec",
            "range": "stddev: 0.000014053755087470774",
            "extra": "mean: 5.088697654822241 msec\nrounds: 197"
          }
        ]
      },
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
          "id": "ac387a080e781a0a38d4ce4e82062b93d6cb55ef",
          "message": "test: Déclencher workflow pour tester SonarQube avec le nouveau token",
          "timestamp": "2025-09-11T17:01:59+02:00",
          "tree_id": "929d56d640c3ab39cebfc8c61b2e15c79627f576",
          "url": "https://github.com/ericfunman/Consultator/commit/ac387a080e781a0a38d4ce4e82062b93d6cb55ef"
        },
        "date": 1757603254551,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.5384934154366,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013415789880618387",
            "extra": "mean: 1.0620914673095245 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 295873.842395805,
            "unit": "iter/sec",
            "range": "stddev: 5.017115507236676e-7",
            "extra": "mean: 3.3798188846388486 usec\nrounds: 117842"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158237.01835496695,
            "unit": "iter/sec",
            "range": "stddev: 7.820873477227369e-7",
            "extra": "mean: 6.3196337392855755 usec\nrounds: 70043"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33974.84887753126,
            "unit": "iter/sec",
            "range": "stddev: 0.000001740646692705348",
            "extra": "mean: 29.433537838672613 usec\nrounds: 21116"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.52323031282842,
            "unit": "iter/sec",
            "range": "stddev: 0.000016072540865037464",
            "extra": "mean: 5.088456964645788 msec\nrounds: 198"
          }
        ]
      }
    ]
  }
}