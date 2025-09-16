window.BENCHMARK_DATA = {
  "lastUpdate": 1758023427696,
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
          "id": "02d0ec6ee2e7eda7a300b54783890390ba6b67de",
          "message": "test: Relancer workflow après création du projet SonarCloud",
          "timestamp": "2025-09-11T17:10:42+02:00",
          "tree_id": "929d56d640c3ab39cebfc8c61b2e15c79627f576",
          "url": "https://github.com/ericfunman/Consultator/commit/02d0ec6ee2e7eda7a300b54783890390ba6b67de"
        },
        "date": 1757603699570,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.1201730773228,
            "unit": "iter/sec",
            "range": "stddev: 0.000004307390201710088",
            "extra": "mean: 1.0625635584137454 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 292882.71620204585,
            "unit": "iter/sec",
            "range": "stddev: 5.245156869387274e-7",
            "extra": "mean: 3.4143359941736797 usec\nrounds: 119261"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 165031.4449003227,
            "unit": "iter/sec",
            "range": "stddev: 7.427791306570013e-7",
            "extra": "mean: 6.0594512797484725 usec\nrounds: 108261"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 30091.64195699799,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016973444254393352",
            "extra": "mean: 33.231819035632384 usec\nrounds: 21507"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 197.18675182608231,
            "unit": "iter/sec",
            "range": "stddev: 0.000010530595453360275",
            "extra": "mean: 5.0713346142138125 msec\nrounds: 197"
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
          "id": "c600fe79d1b4f963d26b7aac37f1304b36cf0d43",
          "message": "fix: Ajouter pytest-benchmark pour les tests de performance",
          "timestamp": "2025-09-11T17:18:01+02:00",
          "tree_id": "51aae3be5c82a65d2f548208c940362b681c573f",
          "url": "https://github.com/ericfunman/Consultator/commit/c600fe79d1b4f963d26b7aac37f1304b36cf0d43"
        },
        "date": 1757604131711,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.7912350539626,
            "unit": "iter/sec",
            "range": "stddev: 0.000004926316936039236",
            "extra": "mean: 1.062935072883243 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 290772.5224707158,
            "unit": "iter/sec",
            "range": "stddev: 5.47234219998929e-7",
            "extra": "mean: 3.439114506085119 usec\nrounds: 120701"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156995.76837204353,
            "unit": "iter/sec",
            "range": "stddev: 8.154417765630533e-7",
            "extra": "mean: 6.369598431661113 usec\nrounds: 74600"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34281.12101244571,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016780731253115765",
            "extra": "mean: 29.170574662274074 usec\nrounds: 21470"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 197.1777037096525,
            "unit": "iter/sec",
            "range": "stddev: 0.000008425464801017893",
            "extra": "mean: 5.071567328284322 msec\nrounds: 198"
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
          "id": "02d0ec6ee2e7eda7a300b54783890390ba6b67de",
          "message": "test: Relancer workflow après création du projet SonarCloud",
          "timestamp": "2025-09-11T17:10:42+02:00",
          "tree_id": "929d56d640c3ab39cebfc8c61b2e15c79627f576",
          "url": "https://github.com/ericfunman/Consultator/commit/02d0ec6ee2e7eda7a300b54783890390ba6b67de"
        },
        "date": 1757604236534,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4060303596456,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022191159024050646",
            "extra": "mean: 1.062240911732815 msec\nrounds: 929"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 297428.3532471624,
            "unit": "iter/sec",
            "range": "stddev: 5.184792027775062e-7",
            "extra": "mean: 3.362154243475913 usec\nrounds: 118274"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 160871.00270773028,
            "unit": "iter/sec",
            "range": "stddev: 8.208900813804101e-7",
            "extra": "mean: 6.21616067015381 usec\nrounds: 74488"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34516.861642925825,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017403785990035036",
            "extra": "mean: 28.97134769507495 usec\nrounds: 19195"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.45170545110963,
            "unit": "iter/sec",
            "range": "stddev: 0.000014888825721377824",
            "extra": "mean: 5.090309588831069 msec\nrounds: 197"
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
          "id": "6754c534d66e6ac2cba8c711294e700a8f423e90",
          "message": "fix: Ajouter pytest-benchmark aux dépendances de test",
          "timestamp": "2025-09-12T08:16:44+02:00",
          "tree_id": "583d0c9fb2e7457acd29b3aeb2e38d752aa582bc",
          "url": "https://github.com/ericfunman/Consultator/commit/6754c534d66e6ac2cba8c711294e700a8f423e90"
        },
        "date": 1757658102819,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.5697928724804,
            "unit": "iter/sec",
            "range": "stddev: 0.00000126880328284454",
            "extra": "mean: 1.0620561614973485 msec\nrounds: 935"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 286637.5160399077,
            "unit": "iter/sec",
            "range": "stddev: 4.943566595509602e-7",
            "extra": "mean: 3.488726855492192 usec\nrounds: 116334"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159131.19902557056,
            "unit": "iter/sec",
            "range": "stddev: 7.46013923708908e-7",
            "extra": "mean: 6.284122825212368 usec\nrounds: 104091"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33243.683945622535,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015530804584846194",
            "extra": "mean: 30.08090203347268 usec\nrounds: 20752"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.60528505691676,
            "unit": "iter/sec",
            "range": "stddev: 0.00001679281482801662",
            "extra": "mean: 5.086333257574955 msec\nrounds: 198"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "committer": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "id": "6754c534d66e6ac2cba8c711294e700a8f423e90",
          "message": "fix: Ajouter pytest-benchmark aux dépendances de test",
          "timestamp": "2025-09-12T06:16:44Z",
          "url": "https://github.com/ericfunman/Consultator/commit/6754c534d66e6ac2cba8c711294e700a8f423e90"
        },
        "date": 1757658569459,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.964768999138,
            "unit": "iter/sec",
            "range": "stddev: 0.000004049204944806918",
            "extra": "mean: 1.062739045016165 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 286326.635047551,
            "unit": "iter/sec",
            "range": "stddev: 5.367987166454892e-7",
            "extra": "mean: 3.4925147631966804 usec\nrounds: 123686"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157928.61793864006,
            "unit": "iter/sec",
            "range": "stddev: 7.32596030405117e-7",
            "extra": "mean: 6.3319746164595045 usec\nrounds: 102271"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33547.511318229524,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016907525718011364",
            "extra": "mean: 29.808470455947226 usec\nrounds: 19564"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.47113549672198,
            "unit": "iter/sec",
            "range": "stddev: 0.000014465755448890906",
            "extra": "mean: 5.089806181817911 msec\nrounds: 198"
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
          "id": "95e7ae84b0350c4082b216b6802773c7f40d62f6",
          "message": "fix: Ajouter la méthode _extract_pylint_score manquante",
          "timestamp": "2025-09-12T08:36:47+02:00",
          "tree_id": "8b84b6ec1087189ad2f9737f999d071e9069eeb4",
          "url": "https://github.com/ericfunman/Consultator/commit/95e7ae84b0350c4082b216b6802773c7f40d62f6"
        },
        "date": 1757659261880,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4540106624925,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017778934025549198",
            "extra": "mean: 1.062186775641127 msec\nrounds: 936"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 296832.6955652525,
            "unit": "iter/sec",
            "range": "stddev: 5.027377845248322e-7",
            "extra": "mean: 3.3689011181727144 usec\nrounds: 125392"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157772.32533300063,
            "unit": "iter/sec",
            "range": "stddev: 7.447125151570487e-7",
            "extra": "mean: 6.338247204567465 usec\nrounds: 104189"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34061.77423592775,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018314398282784295",
            "extra": "mean: 29.358423700231622 usec\nrounds: 20734"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.50405608340276,
            "unit": "iter/sec",
            "range": "stddev: 0.00001489502764281414",
            "extra": "mean: 5.088953479797726 msec\nrounds: 198"
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
          "id": "b38db1c1ca6f2c1d50a53ff89cf7e0eb5f1ab81c",
          "message": "fix: Afficher le nombre réel de tests exécutés dans les logs",
          "timestamp": "2025-09-12T08:44:33+02:00",
          "tree_id": "677f5c37057d03c50de0cbfc1c34070c7e0c59fe",
          "url": "https://github.com/ericfunman/Consultator/commit/b38db1c1ca6f2c1d50a53ff89cf7e0eb5f1ab81c"
        },
        "date": 1757659719547,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2867705732166,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019335815279287513",
            "extra": "mean: 1.0623754962486391 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 292383.7019685618,
            "unit": "iter/sec",
            "range": "stddev: 5.498629140054691e-7",
            "extra": "mean: 3.4201632760895944 usec\nrounds: 119105"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158544.54939274382,
            "unit": "iter/sec",
            "range": "stddev: 7.663613125165068e-7",
            "extra": "mean: 6.307375459012579 usec\nrounds: 66721"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34417.10579068937,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018706213194386424",
            "extra": "mean: 29.05531935432303 usec\nrounds: 21747"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.5316364168055,
            "unit": "iter/sec",
            "range": "stddev: 0.000014400440577231887",
            "extra": "mean: 5.088239319796808 msec\nrounds: 197"
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
          "id": "85932c71a4c9eb5e243e0283d891cc2a4a9b19c7",
          "message": "debug: Ajouter diagnostic du nombre de tests collectés",
          "timestamp": "2025-09-12T08:50:27+02:00",
          "tree_id": "2a51eb6ceed756c32f481f91e999dc73191ba76a",
          "url": "https://github.com/ericfunman/Consultator/commit/85932c71a4c9eb5e243e0283d891cc2a4a9b19c7"
        },
        "date": 1757660079255,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.6049880670388,
            "unit": "iter/sec",
            "range": "stddev: 0.000002525478324670452",
            "extra": "mean: 1.0620164640937562 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 295968.52808290586,
            "unit": "iter/sec",
            "range": "stddev: 5.025839814301002e-7",
            "extra": "mean: 3.378737619426491 usec\nrounds: 121419"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158328.21238980957,
            "unit": "iter/sec",
            "range": "stddev: 8.042680268101917e-7",
            "extra": "mean: 6.315993750614484 usec\nrounds: 105286"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33933.70225022989,
            "unit": "iter/sec",
            "range": "stddev: 0.000001703402557932872",
            "extra": "mean: 29.469227749625382 usec\nrounds: 20303"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 197.22601942376602,
            "unit": "iter/sec",
            "range": "stddev: 0.000011520060711270085",
            "extra": "mean: 5.070324914135029 msec\nrounds: 198"
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
          "id": "6bb480ecf2634e61f46439b5bd0796650090c576",
          "message": "fix: Ajuster les versions pytest-faker pour compatibilité Python 3.9",
          "timestamp": "2025-09-12T08:59:00+02:00",
          "tree_id": "f74a7f35d761c8d9f264cc503497d4c531b2a4ac",
          "url": "https://github.com/ericfunman/Consultator/commit/6bb480ecf2634e61f46439b5bd0796650090c576"
        },
        "date": 1757660609923,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2181426392157,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016675174889706164",
            "extra": "mean: 1.0624529582440447 msec\nrounds: 934"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 295246.0283689914,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015791876153981308",
            "extra": "mean: 3.3870057643932947 usec\nrounds: 125079"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158347.50638630398,
            "unit": "iter/sec",
            "range": "stddev: 7.742998954740767e-7",
            "extra": "mean: 6.315224172589139 usec\nrounds: 70245"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33983.866414944976,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016503141305127164",
            "extra": "mean: 29.425727720028743 usec\nrounds: 21544"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.58303772059293,
            "unit": "iter/sec",
            "range": "stddev: 0.000013918516039646811",
            "extra": "mean: 5.086908878787997 msec\nrounds: 198"
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
          "id": "723ab278ab7ae0a0399521d20ac4df027eb4cdf8",
          "message": "debug: Ajouter diagnostic détaillé des tests collectés",
          "timestamp": "2025-09-12T09:04:46+02:00",
          "tree_id": "83c8ce042f7ddcd09ba912f8168659f72a24fed2",
          "url": "https://github.com/ericfunman/Consultator/commit/723ab278ab7ae0a0399521d20ac4df027eb4cdf8"
        },
        "date": 1757660953804,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.1531204123498,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019664408219606286",
            "extra": "mean: 1.0625263608134958 msec\nrounds: 934"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 294640.9853904601,
            "unit": "iter/sec",
            "range": "stddev: 5.22049655548846e-7",
            "extra": "mean: 3.393960954463934 usec\nrounds: 117427"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 155751.19746962067,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011071548080313349",
            "extra": "mean: 6.420496382989609 usec\nrounds: 73127"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33355.57466566519,
            "unit": "iter/sec",
            "range": "stddev: 0.000001684146060887103",
            "extra": "mean: 29.97999614827076 usec\nrounds: 20251"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.5015629778915,
            "unit": "iter/sec",
            "range": "stddev: 0.000015825998550633034",
            "extra": "mean: 5.089018045686031 msec\nrounds: 197"
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
          "id": "d86844474951a7b104f7c2efec4bc09f23a3d43d",
          "message": "debug: Afficher la sortie brute de pytest --collect-only",
          "timestamp": "2025-09-12T09:10:15+02:00",
          "tree_id": "c0cd8b0bd42b0a68087fb1c1a0f41ff0b45d4105",
          "url": "https://github.com/ericfunman/Consultator/commit/d86844474951a7b104f7c2efec4bc09f23a3d43d"
        },
        "date": 1757661281411,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.9596966347467,
            "unit": "iter/sec",
            "range": "stddev: 0.00000336523303384907",
            "extra": "mean: 1.0627447738478122 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 287661.20817306254,
            "unit": "iter/sec",
            "range": "stddev: 5.299702978251592e-7",
            "extra": "mean: 3.4763116179307034 usec\nrounds: 123077"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156191.59827241863,
            "unit": "iter/sec",
            "range": "stddev: 7.711356312437236e-7",
            "extra": "mean: 6.402393029206788 usec\nrounds: 72015"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33267.33763461577,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018330322967147011",
            "extra": "mean: 30.059513958804647 usec\nrounds: 21062"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.44360100228764,
            "unit": "iter/sec",
            "range": "stddev: 0.000015120277022431718",
            "extra": "mean: 5.0905195939080485 msec\nrounds: 197"
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
          "id": "1af911baebd6ba04b01d3707a884ea3731193d47",
          "message": "fix: Rendre les imports dans conftest.py conditionnels pour éviter les erreurs de collection de tests",
          "timestamp": "2025-09-12T09:16:58+02:00",
          "tree_id": "b92f8bd3c627b2777b425aaa37fedb19a7fc0cfc",
          "url": "https://github.com/ericfunman/Consultator/commit/1af911baebd6ba04b01d3707a884ea3731193d47"
        },
        "date": 1757661682909,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4501272781142,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014679230074002856",
            "extra": "mean: 1.062191157051689 msec\nrounds: 936"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 296479.160899587,
            "unit": "iter/sec",
            "range": "stddev: 5.021587591254157e-7",
            "extra": "mean: 3.372918342610545 usec\nrounds: 132909"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158139.12170385997,
            "unit": "iter/sec",
            "range": "stddev: 7.499863211010237e-7",
            "extra": "mean: 6.323545933640982 usec\nrounds: 72485"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34605.54487091992,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016550521625452511",
            "extra": "mean: 28.897103158757954 usec\nrounds: 21559"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.52549920495895,
            "unit": "iter/sec",
            "range": "stddev: 0.0000164550515663039",
            "extra": "mean: 5.088398218274398 msec\nrounds: 197"
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
          "id": "6cc727784de3eb5bb3428544cb620124dd72c5fd",
          "message": "fix: Améliorer la collection de tests en CI avec configuration pytest simplifiée\n\n- Ignorer pytest.ini en CI pour éviter les conflits avec coverage/html reports\n- Ajouter diagnostic avancé des imports pour identifier les modules manquants\n- Configuration spécifique CI pour collecter tous les tests sans dépendances problématiques\n- Ajout de checks sur PYTHONPATH et modules principaux",
          "timestamp": "2025-09-12T09:23:59+02:00",
          "tree_id": "da97c283477bb4726eb3d9102f063083feff025e",
          "url": "https://github.com/ericfunman/Consultator/commit/6cc727784de3eb5bb3428544cb620124dd72c5fd"
        },
        "date": 1757662105005,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.7027772228565,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035770222629218512",
            "extra": "mean: 1.0630350246782525 msec\nrounds: 932"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 288319.5590775963,
            "unit": "iter/sec",
            "range": "stddev: 5.078931684051661e-7",
            "extra": "mean: 3.4683737835866593 usec\nrounds: 123518"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 152459.36505102136,
            "unit": "iter/sec",
            "range": "stddev: 7.780237466670693e-7",
            "extra": "mean: 6.5591247849244585 usec\nrounds: 58100"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33958.86983011033,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016552892039808588",
            "extra": "mean: 29.447387530939842 usec\nrounds: 21846"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.44166309377798,
            "unit": "iter/sec",
            "range": "stddev: 0.000014831691391001512",
            "extra": "mean: 5.090569812181934 msec\nrounds: 197"
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
          "id": "2483a8bf0ea608d74632947920fa001115f76bb6",
          "message": "fix: Retirer les emojis de test_simple.py pour éviter les erreurs d'encodage Unicode en CI",
          "timestamp": "2025-09-12T09:28:51+02:00",
          "tree_id": "7fc53f64eb29add669093ca0e948797def8e1d0d",
          "url": "https://github.com/ericfunman/Consultator/commit/2483a8bf0ea608d74632947920fa001115f76bb6"
        },
        "date": 1757662398541,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.6962395671219,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015421109327747932",
            "extra": "mean: 1.0619135534189657 msec\nrounds: 936"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 292632.2044549871,
            "unit": "iter/sec",
            "range": "stddev: 5.489918172001018e-7",
            "extra": "mean: 3.4172588825705303 usec\nrounds: 115929"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158479.34301406457,
            "unit": "iter/sec",
            "range": "stddev: 7.604140684223123e-7",
            "extra": "mean: 6.309970630754401 usec\nrounds: 105076"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33319.861998259556,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017033597872447228",
            "extra": "mean: 30.012129103422897 usec\nrounds: 22176"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.45586224997598,
            "unit": "iter/sec",
            "range": "stddev: 0.000015289008240967027",
            "extra": "mean: 5.090201883248319 msec\nrounds: 197"
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
          "id": "b8f21fa27db319cb9c6bfa94f08183db64099300",
          "message": "fix: Améliorer diagnostic CI et installation dépendances principales\n\n- Corriger erreur syntaxe dans diagnostic d'import Python\n- Ajouter installation automatique dépendances principales en CI\n- Améliorer verbosité collection pytest avec -v\n- Ajouter test individuel des fichiers de test pour identifier problèmes d'import",
          "timestamp": "2025-09-12T09:36:01+02:00",
          "tree_id": "8d0527429d52512a9ba461877d006ae3ef6b1b13",
          "url": "https://github.com/ericfunman/Consultator/commit/b8f21fa27db319cb9c6bfa94f08183db64099300"
        },
        "date": 1757662882052,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2758012098454,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019324403059995123",
            "extra": "mean: 1.0623878768737867 msec\nrounds: 934"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 294718.6630285824,
            "unit": "iter/sec",
            "range": "stddev: 7.054328307497128e-7",
            "extra": "mean: 3.393066423835595 usec\nrounds: 126024"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 162791.12994458922,
            "unit": "iter/sec",
            "range": "stddev: 7.405595182688446e-7",
            "extra": "mean: 6.142840831317896 usec\nrounds: 75109"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34194.438002258874,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027232423428820125",
            "extra": "mean: 29.244522162754663 usec\nrounds: 21861"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.4044820681158,
            "unit": "iter/sec",
            "range": "stddev: 0.000014789700651603693",
            "extra": "mean: 5.091533500000199 msec\nrounds: 198"
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
          "id": "860d925996ac0eff3c21be2e4acc8af975e69cf0",
          "message": "fix: MAJOR - Corriger .gitignore qui excluait tous les fichiers test_*.py\n\n CORRECTION CRITIQUE:\n- Le .gitignore bloquait tous les test_*.py empêchant leur versioning\n- Ajouter 38 fichiers de test qui étaient ignorés\n- Le CI ne voyait que 2 tests car les autres n'étaient pas dans le repo\n- Maintenant tous les 260+ tests seront disponibles en CI\n\nCette correction devrait résoudre le problème de collection de tests en CI/CD",
          "timestamp": "2025-09-12T09:37:29+02:00",
          "tree_id": "4ec99ce7b9a482c7642b148d18d3c5c007af79d4",
          "url": "https://github.com/ericfunman/Consultator/commit/860d925996ac0eff3c21be2e4acc8af975e69cf0"
        },
        "date": 1757662916100,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4935372446332,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015327969482476497",
            "extra": "mean: 1.062142182012838 msec\nrounds: 934"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 295373.0055492855,
            "unit": "iter/sec",
            "range": "stddev: 5.311370133976703e-7",
            "extra": "mean: 3.385549732753562 usec\nrounds: 121419"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158430.43077777926,
            "unit": "iter/sec",
            "range": "stddev: 7.519491127752501e-7",
            "extra": "mean: 6.311918708361269 usec\nrounds: 107551"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34047.579378559276,
            "unit": "iter/sec",
            "range": "stddev: 0.000001731962046570854",
            "extra": "mean: 29.370663590543778 usec\nrounds: 21022"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.49215384585318,
            "unit": "iter/sec",
            "range": "stddev: 0.00001668115457340454",
            "extra": "mean: 5.089261736041092 msec\nrounds: 197"
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
          "id": "2f8375b70c92133b163d778718de71f69ef76cd6",
          "message": "feat: Améliorer rapport final avec statistiques détaillées des tests\n\n- Ajouter extraction et stockage des statistiques pytest détaillées\n- Afficher le nombre réel de tests individuels exécutés (267) vs catégories (5)\n- Inclure tests réussis/échoués/ignorés dans le rapport final\n- Séparer les statistiques de catégories vs tests individuels pour plus de clarté",
          "timestamp": "2025-09-12T09:44:56+02:00",
          "tree_id": "ca66e8eebb809f50d8c2b5cc7057c0d51cc468ea",
          "url": "https://github.com/ericfunman/Consultator/commit/2f8375b70c92133b163d778718de71f69ef76cd6"
        },
        "date": 1757663371683,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.8682535741523,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029710056796181303",
            "extra": "mean: 1.0628480620971312 msec\nrounds: 934"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289037.07841014327,
            "unit": "iter/sec",
            "range": "stddev: 7.584280228896321e-7",
            "extra": "mean: 3.4597637282404343 usec\nrounds: 113289"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158341.08567725928,
            "unit": "iter/sec",
            "range": "stddev: 7.899191077984653e-7",
            "extra": "mean: 6.315480254052713 usec\nrounds: 91158"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33350.46525088984,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018116059143999842",
            "extra": "mean: 29.98458919469852 usec\nrounds: 19676"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.43096094889722,
            "unit": "iter/sec",
            "range": "stddev: 0.000015273875374016913",
            "extra": "mean: 5.090847161614998 msec\nrounds: 198"
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
          "id": "587f611881fb3af5a10e6a28f1130c8847e738f2",
          "message": "fix: Pipeline CI/CD - Tests de régression fonctionnels",
          "timestamp": "2025-09-12T09:58:32+02:00",
          "tree_id": "8a4d1b56c871a3408280edb8d7e45272f8c6c6df",
          "url": "https://github.com/ericfunman/Consultator/commit/587f611881fb3af5a10e6a28f1130c8847e738f2"
        },
        "date": 1757664165163,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.9306960299579,
            "unit": "iter/sec",
            "range": "stddev: 0.000004430468627676184",
            "extra": "mean: 1.0627775289075716 msec\nrounds: 934"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 298084.75518812315,
            "unit": "iter/sec",
            "range": "stddev: 5.231030500285269e-7",
            "extra": "mean: 3.3547505620302314 usec\nrounds: 120106"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 155874.39130388672,
            "unit": "iter/sec",
            "range": "stddev: 7.178488027844359e-7",
            "extra": "mean: 6.415422005083815 usec\nrounds: 73992"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33205.68516748242,
            "unit": "iter/sec",
            "range": "stddev: 0.00000158405069418654",
            "extra": "mean: 30.11532497993077 usec\nrounds: 22426"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.42359322067298,
            "unit": "iter/sec",
            "range": "stddev: 0.000015228690422083485",
            "extra": "mean: 5.0910381161622755 msec\nrounds: 198"
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
          "id": "78651c5748c67c8070e26bdc80c5fb4086df5293",
          "message": "feat: Amélioration majeure de la documentation et couverture de tests\n\n- Documentation: Amélioration du ratio de 12.8% à 91.0% (objectif dépassé)\n- Docstrings: Ajout de docstrings détaillées à tous les modules principaux\n- Business Managers: Documentation complète (100% des fonctions)\n- Consultant Services: Amélioration significative de la documentation\n- Tests: 268 tests fonctionnels, couverture à 7% (base solide pour progression)\n- Qualité: Code professionnel avec documentation exhaustive\n\nBREAKING CHANGES: Améliorations de qualité majeures",
          "timestamp": "2025-09-12T18:13:34+02:00",
          "tree_id": "30db24a2958bc2224a06b8f69df9f24a4f288345",
          "url": "https://github.com/ericfunman/Consultator/commit/78651c5748c67c8070e26bdc80c5fb4086df5293"
        },
        "date": 1757693871291,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3018345959775,
            "unit": "iter/sec",
            "range": "stddev: 0.00000258279952189004",
            "extra": "mean: 1.062358494636544 msec\nrounds: 932"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 295226.13487192296,
            "unit": "iter/sec",
            "range": "stddev: 5.324385706092581e-7",
            "extra": "mean: 3.3872339941510496 usec\nrounds: 115661"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158575.0295750549,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010434436132402348",
            "extra": "mean: 6.3061630994474545 usec\nrounds: 104844"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33543.740955992,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018114392507337925",
            "extra": "mean: 29.811820968685595 usec\nrounds: 20259"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.4780969686035,
            "unit": "iter/sec",
            "range": "stddev: 0.000017750284617742305",
            "extra": "mean: 5.089625843433309 msec\nrounds: 198"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "committer": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "id": "78651c5748c67c8070e26bdc80c5fb4086df5293",
          "message": "feat: Amélioration majeure de la documentation et couverture de tests\n\n- Documentation: Amélioration du ratio de 12.8% à 91.0% (objectif dépassé)\n- Docstrings: Ajout de docstrings détaillées à tous les modules principaux\n- Business Managers: Documentation complète (100% des fonctions)\n- Consultant Services: Amélioration significative de la documentation\n- Tests: 268 tests fonctionnels, couverture à 7% (base solide pour progression)\n- Qualité: Code professionnel avec documentation exhaustive\n\nBREAKING CHANGES: Améliorations de qualité majeures",
          "timestamp": "2025-09-12T16:13:34Z",
          "url": "https://github.com/ericfunman/Consultator/commit/78651c5748c67c8070e26bdc80c5fb4086df5293"
        },
        "date": 1757744777155,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.233596674404,
            "unit": "iter/sec",
            "range": "stddev: 0.000001659386652032481",
            "extra": "mean: 1.0624355139183634 msec\nrounds: 934"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 292987.407231173,
            "unit": "iter/sec",
            "range": "stddev: 5.150979118294241e-7",
            "extra": "mean: 3.4131159746772997 usec\nrounds: 116741"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158312.3823968934,
            "unit": "iter/sec",
            "range": "stddev: 8.463779230328224e-7",
            "extra": "mean: 6.31662530030641 usec\nrounds: 64521"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34232.672956687406,
            "unit": "iter/sec",
            "range": "stddev: 0.000001780525893773831",
            "extra": "mean: 29.211858544182085 usec\nrounds: 20593"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.51380851320545,
            "unit": "iter/sec",
            "range": "stddev: 0.000015900452897661648",
            "extra": "mean: 5.0887009292927186 msec\nrounds: 198"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "committer": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "id": "78651c5748c67c8070e26bdc80c5fb4086df5293",
          "message": "feat: Amélioration majeure de la documentation et couverture de tests\n\n- Documentation: Amélioration du ratio de 12.8% à 91.0% (objectif dépassé)\n- Docstrings: Ajout de docstrings détaillées à tous les modules principaux\n- Business Managers: Documentation complète (100% des fonctions)\n- Consultant Services: Amélioration significative de la documentation\n- Tests: 268 tests fonctionnels, couverture à 7% (base solide pour progression)\n- Qualité: Code professionnel avec documentation exhaustive\n\nBREAKING CHANGES: Améliorations de qualité majeures",
          "timestamp": "2025-09-12T16:13:34Z",
          "url": "https://github.com/ericfunman/Consultator/commit/78651c5748c67c8070e26bdc80c5fb4086df5293"
        },
        "date": 1757831213077,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.6740128652173,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020350389016464924",
            "extra": "mean: 1.0619386181820132 msec\nrounds: 935"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 285279.24499973736,
            "unit": "iter/sec",
            "range": "stddev: 4.983773534891313e-7",
            "extra": "mean: 3.505337375668253 usec\nrounds: 115527"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156159.6129878721,
            "unit": "iter/sec",
            "range": "stddev: 7.566307958943702e-7",
            "extra": "mean: 6.403704394923568 usec\nrounds: 72015"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33302.38119684014,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015760604031228927",
            "extra": "mean: 30.02788281382365 usec\nrounds: 22716"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.42749693522902,
            "unit": "iter/sec",
            "range": "stddev: 0.000014793032146818667",
            "extra": "mean: 5.090936939087224 msec\nrounds: 197"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "committer": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "id": "78651c5748c67c8070e26bdc80c5fb4086df5293",
          "message": "feat: Amélioration majeure de la documentation et couverture de tests\n\n- Documentation: Amélioration du ratio de 12.8% à 91.0% (objectif dépassé)\n- Docstrings: Ajout de docstrings détaillées à tous les modules principaux\n- Business Managers: Documentation complète (100% des fonctions)\n- Consultant Services: Amélioration significative de la documentation\n- Tests: 268 tests fonctionnels, couverture à 7% (base solide pour progression)\n- Qualité: Code professionnel avec documentation exhaustive\n\nBREAKING CHANGES: Améliorations de qualité majeures",
          "timestamp": "2025-09-12T16:13:34Z",
          "url": "https://github.com/ericfunman/Consultator/commit/78651c5748c67c8070e26bdc80c5fb4086df5293"
        },
        "date": 1757917879194,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2736485313452,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033043597647092103",
            "extra": "mean: 1.0623903065386826 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289262.26767703146,
            "unit": "iter/sec",
            "range": "stddev: 6.347973783956225e-7",
            "extra": "mean: 3.4570703190245498 usec\nrounds: 112146"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158430.1869997089,
            "unit": "iter/sec",
            "range": "stddev: 7.483710079748037e-7",
            "extra": "mean: 6.311928420572005 usec\nrounds: 104625"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34302.69196825404,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035961921918136134",
            "extra": "mean: 29.152230994741334 usec\nrounds: 21836"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.49126525105723,
            "unit": "iter/sec",
            "range": "stddev: 0.000014519066861691013",
            "extra": "mean: 5.089284751270232 msec\nrounds: 197"
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
          "id": "2c1c2607f6abe6a7e7f982dcf8d67e24bdce9279",
          "message": " Fix: Corrections critiques pour Business Managers et Practices\n\n Corrections apportées:\n- Fix erreur 'str' object cannot be interpreted as an integer dans business_managers.py\n- Correction des imports absolus (app.database.database au lieu de database.database)\n- Remplacement de get_session() par get_database_session() dans tous les modules\n- Garantie que les IDs sont des entiers avec int(bm.id) dans les services\n- Fix requête SQL: consultant_competences au lieu de competences dans practice_service_optimized.py\n\n Données de test:\n- Correction génération 1000 consultants avec emails uniques (compteur incrémental)\n- Nouveau script create_basic_test_data.py pour génération rapide de données de test\n- Scripts fonctionnels avec toutes les relations (consultants, missions, CVs, compétences)\n\n Impact:\n- Navigation Business Managers maintenant fonctionnelle\n- Pages Practices accessibles sans erreur SQL\n- Base de données avec 1000 consultants, 12433 missions, 1986 CVs\n- Application stable et opérationnelle",
          "timestamp": "2025-09-15T11:24:43+02:00",
          "tree_id": "5abfef29d2fb1eba5b85115a1f561adce5b4b5fa",
          "url": "https://github.com/ericfunman/Consultator/commit/2c1c2607f6abe6a7e7f982dcf8d67e24bdce9279"
        },
        "date": 1757928539016,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.6619200276491,
            "unit": "iter/sec",
            "range": "stddev: 0.000001505077898916033",
            "extra": "mean: 1.0619522556148793 msec\nrounds: 935"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 279174.62100568245,
            "unit": "iter/sec",
            "range": "stddev: 5.187317923185793e-7",
            "extra": "mean: 3.5819874901151767 usec\nrounds: 107435"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158191.2603558258,
            "unit": "iter/sec",
            "range": "stddev: 7.698011717769505e-7",
            "extra": "mean: 6.321461740368342 usec\nrounds: 104745"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 34548.775925692695,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016794999272954902",
            "extra": "mean: 28.944585537582988 usec\nrounds: 22873"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.59182641701062,
            "unit": "iter/sec",
            "range": "stddev: 0.000013908124804513295",
            "extra": "mean: 5.086681467004634 msec\nrounds: 197"
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
          "id": "3514d290d85133ff7bbefd060458fb9e886f2602",
          "message": " Corrections majeures et optimisation\n\n- Correction des tests en erreur (20 tests corrigés)\n- Restructuration complète des tests (UI, unit, integration)\n- Optimisation des performances des services\n- Mise à jour de la documentation\n- Ajout de workflows CI/CD\n- Nettoyage des fichiers obsolètes\n- Amélioration de la couverture de test",
          "timestamp": "2025-09-15T15:10:44+02:00",
          "tree_id": "add005d30b1ef9fbb892a9c9b3c7e12eaf347a9f",
          "url": "https://github.com/ericfunman/Consultator/commit/3514d290d85133ff7bbefd060458fb9e886f2602"
        },
        "date": 1757942104601,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.0821667664322,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021477407144147157",
            "extra": "mean: 1.0626064708419776 msec\nrounds: 926"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 296177.97054414975,
            "unit": "iter/sec",
            "range": "stddev: 5.605434267637219e-7",
            "extra": "mean: 3.376348342730423 usec\nrounds: 108732"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 154300.8088499514,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015370757540279186",
            "extra": "mean: 6.480847426875397 usec\nrounds: 76075"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33151.46614741857,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018639744616423812",
            "extra": "mean: 30.164578409690264 usec\nrounds: 19564"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.27854699219472,
            "unit": "iter/sec",
            "range": "stddev: 0.00001829168283338662",
            "extra": "mean: 5.094800299493588 msec\nrounds: 197"
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
          "id": "3514d290d85133ff7bbefd060458fb9e886f2602",
          "message": " Corrections majeures et optimisation\n\n- Correction des tests en erreur (20 tests corrigés)\n- Restructuration complète des tests (UI, unit, integration)\n- Optimisation des performances des services\n- Mise à jour de la documentation\n- Ajout de workflows CI/CD\n- Nettoyage des fichiers obsolètes\n- Amélioration de la couverture de test",
          "timestamp": "2025-09-15T15:10:44+02:00",
          "tree_id": "add005d30b1ef9fbb892a9c9b3c7e12eaf347a9f",
          "url": "https://github.com/ericfunman/Consultator/commit/3514d290d85133ff7bbefd060458fb9e886f2602"
        },
        "date": 1757942114394,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.8840848967878,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028470003402055766",
            "extra": "mean: 1.0628301786077048 msec\nrounds: 935"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 294757.6408424722,
            "unit": "iter/sec",
            "range": "stddev: 5.516265769309313e-7",
            "extra": "mean: 3.392617735512517 usec\nrounds: 114065"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158861.07515130728,
            "unit": "iter/sec",
            "range": "stddev: 7.823977087738615e-7",
            "extra": "mean: 6.294808209295762 usec\nrounds: 71552"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32751.635339337387,
            "unit": "iter/sec",
            "range": "stddev: 0.000001809704205660594",
            "extra": "mean: 30.532826518098123 usec\nrounds: 21374"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.40218004594797,
            "unit": "iter/sec",
            "range": "stddev: 0.00001520004319121796",
            "extra": "mean: 5.091593177662547 msec\nrounds: 197"
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
          "id": "8b4620c1e37847c21fe6873d31c5a58405cc8c2e",
          "message": " Amélioration majeure de la suite de tests\n\n Corrections des erreurs de syntaxe et lint\n- Correction des erreurs E722 (bare except clauses)\n- Résolution des erreurs de syntaxe dans test_skill_categories.py et test_technologies_referentiel.py\n- Amélioration de la gestion d'erreurs avec Exception explicite\n\n Amélioration des services\n- Ajout des paramètres manquants (practice_filter, grade_filter, availability_filter) dans ConsultantService\n- Correction des méthodes search_consultants_optimized et get_all_consultants_with_stats\n\n Résultats des tests\n- 412 tests collectés (vs 311 précédemment)\n- 382 tests réussis (énorme amélioration !)\n- Réduction significative des échecs (30 restants vs centaines)\n\n Amélioration de l'infrastructure de test\n- Correction des données de test avec noms uniques\n- Amélioration du nettoyage des données de test\n- Meilleure isolation des tests\n\n Prochaines étapes: Finalisation des 30 tests restants",
          "timestamp": "2025-09-15T17:40:41+02:00",
          "tree_id": "88286ab31a1bd2816aa4e5064b2899a6038a0404",
          "url": "https://github.com/ericfunman/Consultator/commit/8b4620c1e37847c21fe6873d31c5a58405cc8c2e"
        },
        "date": 1757951098900,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.5060280997894,
            "unit": "iter/sec",
            "range": "stddev: 0.0000056339043768967616",
            "extra": "mean: 1.0632574062501363 msec\nrounds: 928"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 291624.654387441,
            "unit": "iter/sec",
            "range": "stddev: 5.227670258808441e-7",
            "extra": "mean: 3.4290653583473762 usec\nrounds: 116741"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158511.5071460815,
            "unit": "iter/sec",
            "range": "stddev: 7.55798822205162e-7",
            "extra": "mean: 6.308690252237757 usec\nrounds: 77731"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33850.809989613364,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018025294708033132",
            "extra": "mean: 29.541390599127045 usec\nrounds: 21147"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.45237760318318,
            "unit": "iter/sec",
            "range": "stddev: 0.000014704876491579814",
            "extra": "mean: 5.090292172589092 msec\nrounds: 197"
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
          "id": "8b4620c1e37847c21fe6873d31c5a58405cc8c2e",
          "message": " Amélioration majeure de la suite de tests\n\n Corrections des erreurs de syntaxe et lint\n- Correction des erreurs E722 (bare except clauses)\n- Résolution des erreurs de syntaxe dans test_skill_categories.py et test_technologies_referentiel.py\n- Amélioration de la gestion d'erreurs avec Exception explicite\n\n Amélioration des services\n- Ajout des paramètres manquants (practice_filter, grade_filter, availability_filter) dans ConsultantService\n- Correction des méthodes search_consultants_optimized et get_all_consultants_with_stats\n\n Résultats des tests\n- 412 tests collectés (vs 311 précédemment)\n- 382 tests réussis (énorme amélioration !)\n- Réduction significative des échecs (30 restants vs centaines)\n\n Amélioration de l'infrastructure de test\n- Correction des données de test avec noms uniques\n- Amélioration du nettoyage des données de test\n- Meilleure isolation des tests\n\n Prochaines étapes: Finalisation des 30 tests restants",
          "timestamp": "2025-09-15T17:40:41+02:00",
          "tree_id": "88286ab31a1bd2816aa4e5064b2899a6038a0404",
          "url": "https://github.com/ericfunman/Consultator/commit/8b4620c1e37847c21fe6873d31c5a58405cc8c2e"
        },
        "date": 1757951104857,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.8586942658987,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034211371587436607",
            "extra": "mean: 1.0628588608412084 msec\nrounds: 927"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 274481.6833677679,
            "unit": "iter/sec",
            "range": "stddev: 5.43518097188701e-7",
            "extra": "mean: 3.643230352315119 usec\nrounds: 115128"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 155402.31901768222,
            "unit": "iter/sec",
            "range": "stddev: 7.442029536937746e-7",
            "extra": "mean: 6.434910407522403 usec\nrounds: 75330"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32590.058435834373,
            "unit": "iter/sec",
            "range": "stddev: 0.000002490180019965693",
            "extra": "mean: 30.68420395651856 usec\nrounds: 20877"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.6988687843069,
            "unit": "iter/sec",
            "range": "stddev: 0.000017029791127797203",
            "extra": "mean: 5.083913324873083 msec\nrounds: 197"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "committer": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "id": "8b4620c1e37847c21fe6873d31c5a58405cc8c2e",
          "message": " Amélioration majeure de la suite de tests\n\n Corrections des erreurs de syntaxe et lint\n- Correction des erreurs E722 (bare except clauses)\n- Résolution des erreurs de syntaxe dans test_skill_categories.py et test_technologies_referentiel.py\n- Amélioration de la gestion d'erreurs avec Exception explicite\n\n Amélioration des services\n- Ajout des paramètres manquants (practice_filter, grade_filter, availability_filter) dans ConsultantService\n- Correction des méthodes search_consultants_optimized et get_all_consultants_with_stats\n\n Résultats des tests\n- 412 tests collectés (vs 311 précédemment)\n- 382 tests réussis (énorme amélioration !)\n- Réduction significative des échecs (30 restants vs centaines)\n\n Amélioration de l'infrastructure de test\n- Correction des données de test avec noms uniques\n- Amélioration du nettoyage des données de test\n- Meilleure isolation des tests\n\n Prochaines étapes: Finalisation des 30 tests restants",
          "timestamp": "2025-09-15T15:40:41Z",
          "url": "https://github.com/ericfunman/Consultator/commit/8b4620c1e37847c21fe6873d31c5a58405cc8c2e"
        },
        "date": 1758004246856,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.0961391667058,
            "unit": "iter/sec",
            "range": "stddev: 0.000001925962131217398",
            "extra": "mean: 1.0625906943847956 msec\nrounds: 926"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 287429.61649138737,
            "unit": "iter/sec",
            "range": "stddev: 6.63238535326743e-7",
            "extra": "mean: 3.479112598788039 usec\nrounds: 109566"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157203.28097690217,
            "unit": "iter/sec",
            "range": "stddev: 7.869938384565762e-7",
            "extra": "mean: 6.361190388557664 usec\nrounds: 77137"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33049.12377377294,
            "unit": "iter/sec",
            "range": "stddev: 0.000002049398210781848",
            "extra": "mean: 30.257988285716007 usec\nrounds: 26976"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.6583366221426,
            "unit": "iter/sec",
            "range": "stddev: 0.00001755879611638976",
            "extra": "mean: 5.08496114213246 msec\nrounds: 197"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "committer": {
            "name": "Eric Funman",
            "username": "ericfunman",
            "email": "lapinae@gmail.com"
          },
          "id": "8b4620c1e37847c21fe6873d31c5a58405cc8c2e",
          "message": " Amélioration majeure de la suite de tests\n\n Corrections des erreurs de syntaxe et lint\n- Correction des erreurs E722 (bare except clauses)\n- Résolution des erreurs de syntaxe dans test_skill_categories.py et test_technologies_referentiel.py\n- Amélioration de la gestion d'erreurs avec Exception explicite\n\n Amélioration des services\n- Ajout des paramètres manquants (practice_filter, grade_filter, availability_filter) dans ConsultantService\n- Correction des méthodes search_consultants_optimized et get_all_consultants_with_stats\n\n Résultats des tests\n- 412 tests collectés (vs 311 précédemment)\n- 382 tests réussis (énorme amélioration !)\n- Réduction significative des échecs (30 restants vs centaines)\n\n Amélioration de l'infrastructure de test\n- Correction des données de test avec noms uniques\n- Amélioration du nettoyage des données de test\n- Meilleure isolation des tests\n\n Prochaines étapes: Finalisation des 30 tests restants",
          "timestamp": "2025-09-15T15:40:41Z",
          "url": "https://github.com/ericfunman/Consultator/commit/8b4620c1e37847c21fe6873d31c5a58405cc8c2e"
        },
        "date": 1758004806953,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4370069982575,
            "unit": "iter/sec",
            "range": "stddev: 0.00000279162983653318",
            "extra": "mean: 1.062205960214448 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 293486.62653110025,
            "unit": "iter/sec",
            "range": "stddev: 5.797177963116603e-7",
            "extra": "mean: 3.407310281288172 usec\nrounds: 112398"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158714.6359552798,
            "unit": "iter/sec",
            "range": "stddev: 7.036401149098934e-7",
            "extra": "mean: 6.300616159191296 usec\nrounds: 76081"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32683.648373679895,
            "unit": "iter/sec",
            "range": "stddev: 0.000002312500254295953",
            "extra": "mean: 30.59633944677054 usec\nrounds: 27153"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.45981964927515,
            "unit": "iter/sec",
            "range": "stddev: 0.000014481519047094051",
            "extra": "mean: 5.0900993484836965 msec\nrounds: 198"
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
          "id": "22438679749605b6d7e3c98aece41c8ceb9d3267",
          "message": " Correction CI/CD - Tests simples et dépendances\n\n Corrections des erreurs CI/CD GitHub Actions :\n\n1. **Correction test_simple.py** :\n   - Fonctions de test retournent maintenant True/False au lieu de None\n   - Gestion correcte des résultats dans sum(results)\n   - Évite TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'\n\n2. **Ajout dépendance manquante** :\n   - Ajout de openpyxl>=3.1.0 dans requirements.txt\n   - Corrige les tests d'export Excel qui échouaient dans CI\n\n3. **Résultats attendus** :\n   -  Tests unitaires : OK\n   -  Tests de fumée : OK\n   -  Tests de régression : OK\n   -  Pipeline qualité complet : OK\n\n Le CI/CD devrait maintenant passer avec succès sur GitHub Actions",
          "timestamp": "2025-09-16T12:50:45+02:00",
          "tree_id": "7701b036153701b0e7219fbcb1c8d9c6e077c0a2",
          "url": "https://github.com/ericfunman/Consultator/commit/22438679749605b6d7e3c98aece41c8ceb9d3267"
        },
        "date": 1758020768928,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4737247814519,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022168578536939375",
            "extra": "mean: 1.0621645338345838 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289055.71369710955,
            "unit": "iter/sec",
            "range": "stddev: 5.295547165752841e-7",
            "extra": "mean: 3.459540678887468 usec\nrounds: 113302"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 160698.49068227565,
            "unit": "iter/sec",
            "range": "stddev: 7.407048024061564e-7",
            "extra": "mean: 6.222833803567862 usec\nrounds: 79033"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33639.63720316864,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017236301634429679",
            "extra": "mean: 29.726836646912663 usec\nrounds: 28117"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.4183428258282,
            "unit": "iter/sec",
            "range": "stddev: 0.000018632999522608046",
            "extra": "mean: 5.091174203046499 msec\nrounds: 197"
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
          "id": "22438679749605b6d7e3c98aece41c8ceb9d3267",
          "message": " Correction CI/CD - Tests simples et dépendances\n\n Corrections des erreurs CI/CD GitHub Actions :\n\n1. **Correction test_simple.py** :\n   - Fonctions de test retournent maintenant True/False au lieu de None\n   - Gestion correcte des résultats dans sum(results)\n   - Évite TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'\n\n2. **Ajout dépendance manquante** :\n   - Ajout de openpyxl>=3.1.0 dans requirements.txt\n   - Corrige les tests d'export Excel qui échouaient dans CI\n\n3. **Résultats attendus** :\n   -  Tests unitaires : OK\n   -  Tests de fumée : OK\n   -  Tests de régression : OK\n   -  Pipeline qualité complet : OK\n\n Le CI/CD devrait maintenant passer avec succès sur GitHub Actions",
          "timestamp": "2025-09-16T12:50:45+02:00",
          "tree_id": "7701b036153701b0e7219fbcb1c8d9c6e077c0a2",
          "url": "https://github.com/ericfunman/Consultator/commit/22438679749605b6d7e3c98aece41c8ceb9d3267"
        },
        "date": 1758020769687,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.7394349158648,
            "unit": "iter/sec",
            "range": "stddev: 0.000005600590679405604",
            "extra": "mean: 1.0629936015060697 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 290556.35826379334,
            "unit": "iter/sec",
            "range": "stddev: 5.488070185923388e-7",
            "extra": "mean: 3.4416730921858183 usec\nrounds: 120251"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 160575.75770207107,
            "unit": "iter/sec",
            "range": "stddev: 7.415451259678097e-7",
            "extra": "mean: 6.22759010644296 usec\nrounds: 79911"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33181.56396791269,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017398214583688504",
            "extra": "mean: 30.137217189853445 usec\nrounds: 27888"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.7968734583527,
            "unit": "iter/sec",
            "range": "stddev: 0.00001578619554532993",
            "extra": "mean: 5.081381540401482 msec\nrounds: 198"
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
          "id": "d928792c14b16532d2c92c830499ed69cf17eab0",
          "message": " Correction SonarCloud - Configuration couverture de code\n\n Correction de l'intégration SonarCloud pour la couverture de code :\n\n1. **Workflow SonarCloud corrigé** :\n   - Génération du rapport XML dans \reports/coverage.xml (au lieu du répertoire racine)\n   - Ajout de mkdir -p reports pour s'assurer que le répertoire existe\n   - Génération du rapport HTML en complément\n   - Version Python alignée sur 3.10 (comme dans CI principal)\n\n2. **Dépendances de test ajoutées** :\n   - pytest-xdist pour l'exécution parallèle\n   - \faker pour les données de test\n\n3. **Configuration validée** :\n   - Rapport XML généré au bon endroit (\reports/coverage.xml)\n   - Compatible avec sonar.python.coverage.reportPaths=reports/coverage.xml\n   - Tests locaux :  couverture détectée et rapport généré\n\n Résultat attendu :\n- SonarCloud détectera maintenant la couverture de code (au lieu de 0%)\n- Métriques de couverture précises (~36% global)\n- Visibilité des zones couvertes/non couvertes par module\n\n Prochaine analyse SonarCloud devrait afficher la couverture correcte",
          "timestamp": "2025-09-16T13:23:05+02:00",
          "tree_id": "f939da1887252fc31b2cc48340a345e0fd9d90be",
          "url": "https://github.com/ericfunman/Consultator/commit/d928792c14b16532d2c92c830499ed69cf17eab0"
        },
        "date": 1758022069189,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2201676250929,
            "unit": "iter/sec",
            "range": "stddev: 0.000002886143951162945",
            "extra": "mean: 1.0624506724321703 msec\nrounds: 925"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 274504.4623444847,
            "unit": "iter/sec",
            "range": "stddev: 9.404667609043322e-7",
            "extra": "mean: 3.6429280291446307 usec\nrounds: 114338"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158333.49542677632,
            "unit": "iter/sec",
            "range": "stddev: 9.105127015524798e-7",
            "extra": "mean: 6.315783007913604 usec\nrounds: 77436"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32671.26004653319,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018386360723991192",
            "extra": "mean: 30.60794100306247 usec\nrounds: 27459"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.44307915590198,
            "unit": "iter/sec",
            "range": "stddev: 0.000015639163361103677",
            "extra": "mean: 5.090533116752745 msec\nrounds: 197"
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
          "id": "d928792c14b16532d2c92c830499ed69cf17eab0",
          "message": " Correction SonarCloud - Configuration couverture de code\n\n Correction de l'intégration SonarCloud pour la couverture de code :\n\n1. **Workflow SonarCloud corrigé** :\n   - Génération du rapport XML dans \reports/coverage.xml (au lieu du répertoire racine)\n   - Ajout de mkdir -p reports pour s'assurer que le répertoire existe\n   - Génération du rapport HTML en complément\n   - Version Python alignée sur 3.10 (comme dans CI principal)\n\n2. **Dépendances de test ajoutées** :\n   - pytest-xdist pour l'exécution parallèle\n   - \faker pour les données de test\n\n3. **Configuration validée** :\n   - Rapport XML généré au bon endroit (\reports/coverage.xml)\n   - Compatible avec sonar.python.coverage.reportPaths=reports/coverage.xml\n   - Tests locaux :  couverture détectée et rapport généré\n\n Résultat attendu :\n- SonarCloud détectera maintenant la couverture de code (au lieu de 0%)\n- Métriques de couverture précises (~36% global)\n- Visibilité des zones couvertes/non couvertes par module\n\n Prochaine analyse SonarCloud devrait afficher la couverture correcte",
          "timestamp": "2025-09-16T13:23:05+02:00",
          "tree_id": "f939da1887252fc31b2cc48340a345e0fd9d90be",
          "url": "https://github.com/ericfunman/Consultator/commit/d928792c14b16532d2c92c830499ed69cf17eab0"
        },
        "date": 1758022075109,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.6387332812217,
            "unit": "iter/sec",
            "range": "stddev: 0.000001168934323476321",
            "extra": "mean: 1.0619784049403038 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 292269.5928895746,
            "unit": "iter/sec",
            "range": "stddev: 4.84133041320409e-7",
            "extra": "mean: 3.42149859009733 usec\nrounds: 110291"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 149644.06667909503,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016278380058961416",
            "extra": "mean: 6.682523551999258 usec\nrounds: 78040"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33200.855484817934,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017483335940606333",
            "extra": "mean: 30.119705814727553 usec\nrounds: 27843"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.50841709832133,
            "unit": "iter/sec",
            "range": "stddev: 0.000014325467782871987",
            "extra": "mean: 5.088840543149144 msec\nrounds: 197"
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
          "id": "30e7147182ba7354f6bff841bbc7efb8cd562463",
          "message": "Fix SonarCloud workflow: use .NET scanner CLI instead of GitHub action\n\n- Replace problematic GitHub action with direct .NET SonarScanner CLI\n- Configure proper coverage report path and project settings\n- Ensure SonarCloud can read coverage.xml from reports/ directory",
          "timestamp": "2025-09-16T13:29:51+02:00",
          "tree_id": "b703d2daacd5ab32267415e3648d2965233bbe76",
          "url": "https://github.com/ericfunman/Consultator/commit/30e7147182ba7354f6bff841bbc7efb8cd562463"
        },
        "date": 1758022457975,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.0550079451187,
            "unit": "iter/sec",
            "range": "stddev: 0.000003013145662525636",
            "extra": "mean: 1.0626371376351242 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 286300.5685960321,
            "unit": "iter/sec",
            "range": "stddev: 4.919896982648289e-7",
            "extra": "mean: 3.492832741841293 usec\nrounds: 112778"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159508.4998417942,
            "unit": "iter/sec",
            "range": "stddev: 6.83561590075459e-7",
            "extra": "mean: 6.269258384298222 usec\nrounds: 79854"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32722.119642170277,
            "unit": "iter/sec",
            "range": "stddev: 0.000002454089195893065",
            "extra": "mean: 30.56036744976816 usec\nrounds: 28559"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.5272940784434,
            "unit": "iter/sec",
            "range": "stddev: 0.000015961307447570974",
            "extra": "mean: 5.088351746199957 msec\nrounds: 197"
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
          "id": "30e7147182ba7354f6bff841bbc7efb8cd562463",
          "message": "Fix SonarCloud workflow: use .NET scanner CLI instead of GitHub action\n\n- Replace problematic GitHub action with direct .NET SonarScanner CLI\n- Configure proper coverage report path and project settings\n- Ensure SonarCloud can read coverage.xml from reports/ directory",
          "timestamp": "2025-09-16T13:29:51+02:00",
          "tree_id": "b703d2daacd5ab32267415e3648d2965233bbe76",
          "url": "https://github.com/ericfunman/Consultator/commit/30e7147182ba7354f6bff841bbc7efb8cd562463"
        },
        "date": 1758022480598,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2718594502345,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024830106733789073",
            "extra": "mean: 1.0623923258303574 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 283716.29283896985,
            "unit": "iter/sec",
            "range": "stddev: 5.159840996198993e-7",
            "extra": "mean: 3.5246477739915156 usec\nrounds: 129133"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159084.75878189286,
            "unit": "iter/sec",
            "range": "stddev: 7.042386963636301e-7",
            "extra": "mean: 6.285957295073202 usec\nrounds: 81747"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33370.60600360788,
            "unit": "iter/sec",
            "range": "stddev: 0.000002134174133919444",
            "extra": "mean: 29.966492064659676 usec\nrounds: 28543"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.42502231754054,
            "unit": "iter/sec",
            "range": "stddev: 0.00001626367291752568",
            "extra": "mean: 5.09100107614294 msec\nrounds: 197"
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
          "id": "f9b65722371c988b57657fe39cb62dd5e4da39cf",
          "message": "Fix SonarCloud workflow: use Java-based scanner for Python project\n\n- Replace .NET scanner with official SonarQube CLI scanner\n- Remove dotnet build step (not needed for Python)\n- Use proper sonar-scanner command for Python analysis\n- Configure correct coverage report path for Python",
          "timestamp": "2025-09-16T13:32:58+02:00",
          "tree_id": "1ab3804e1623235672066e6616f85ae53bc9db91",
          "url": "https://github.com/ericfunman/Consultator/commit/f9b65722371c988b57657fe39cb62dd5e4da39cf"
        },
        "date": 1758022830192,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3743621667921,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021572926205592594",
            "extra": "mean: 1.062276645922529 msec\nrounds: 932"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 281631.218929137,
            "unit": "iter/sec",
            "range": "stddev: 5.424824134640595e-7",
            "extra": "mean: 3.550742718802124 usec\nrounds: 110902"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158565.9532213804,
            "unit": "iter/sec",
            "range": "stddev: 7.579382310178106e-7",
            "extra": "mean: 6.306524065754893 usec\nrounds: 77496"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32063.023403266478,
            "unit": "iter/sec",
            "range": "stddev: 0.000005875093896107057",
            "extra": "mean: 31.188574683762457 usec\nrounds: 27429"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.50437123524424,
            "unit": "iter/sec",
            "range": "stddev: 0.000015162106863870314",
            "extra": "mean: 5.088945318182541 msec\nrounds: 198"
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
          "id": "f9b65722371c988b57657fe39cb62dd5e4da39cf",
          "message": "Fix SonarCloud workflow: use Java-based scanner for Python project\n\n- Replace .NET scanner with official SonarQube CLI scanner\n- Remove dotnet build step (not needed for Python)\n- Use proper sonar-scanner command for Python analysis\n- Configure correct coverage report path for Python",
          "timestamp": "2025-09-16T13:32:58+02:00",
          "tree_id": "1ab3804e1623235672066e6616f85ae53bc9db91",
          "url": "https://github.com/ericfunman/Consultator/commit/f9b65722371c988b57657fe39cb62dd5e4da39cf"
        },
        "date": 1758022834914,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.382294455369,
            "unit": "iter/sec",
            "range": "stddev: 0.00000200044289874105",
            "extra": "mean: 1.0622676949522871 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 295081.0620953577,
            "unit": "iter/sec",
            "range": "stddev: 5.169589892747747e-7",
            "extra": "mean: 3.3888992838071132 usec\nrounds: 116605"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158669.48844273612,
            "unit": "iter/sec",
            "range": "stddev: 7.410027564753684e-7",
            "extra": "mean: 6.302408924453679 usec\nrounds: 78660"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33417.8624047184,
            "unit": "iter/sec",
            "range": "stddev: 0.000004846376029298311",
            "extra": "mean: 29.924116267197455 usec\nrounds: 27626"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.20894439903674,
            "unit": "iter/sec",
            "range": "stddev: 0.000010888612295468857",
            "extra": "mean: 5.096607614208791 msec\nrounds: 197"
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
          "id": "f02a412f5cced96486e2664e4d6c76e6c7b3327e",
          "message": "Fix SonarCloud scanner version for Java 11 compatibility\n\n- Downgrade sonar-scanner-cli from 4.8.0 to 4.7.0 (Java 11 compatible)\n- Version 4.8.0 requires Java 17, but GitHub Actions uses Java 11\n- This should resolve the UnsupportedClassVersionError",
          "timestamp": "2025-09-16T13:38:31+02:00",
          "tree_id": "02c64bc6cd40da8fc308bef86b2ed762432128e1",
          "url": "https://github.com/ericfunman/Consultator/commit/f02a412f5cced96486e2664e4d6c76e6c7b3327e"
        },
        "date": 1758022986195,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3180859381183,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018948500842118534",
            "extra": "mean: 1.0623401535979193 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 302525.9690730772,
            "unit": "iter/sec",
            "range": "stddev: 5.458946570958158e-7",
            "extra": "mean: 3.305501352706826 usec\nrounds: 116064"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 161067.94707130519,
            "unit": "iter/sec",
            "range": "stddev: 7.349193938580702e-7",
            "extra": "mean: 6.208559916376767 usec\nrounds: 107216"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32496.87643695654,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017635152673821878",
            "extra": "mean: 30.772188272924794 usec\nrounds: 28140"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.40513998366464,
            "unit": "iter/sec",
            "range": "stddev: 0.00001458038141869515",
            "extra": "mean: 5.091516444443214 msec\nrounds: 198"
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
          "id": "f02a412f5cced96486e2664e4d6c76e6c7b3327e",
          "message": "Fix SonarCloud scanner version for Java 11 compatibility\n\n- Downgrade sonar-scanner-cli from 4.8.0 to 4.7.0 (Java 11 compatible)\n- Version 4.8.0 requires Java 17, but GitHub Actions uses Java 11\n- This should resolve the UnsupportedClassVersionError",
          "timestamp": "2025-09-16T13:38:31+02:00",
          "tree_id": "02c64bc6cd40da8fc308bef86b2ed762432128e1",
          "url": "https://github.com/ericfunman/Consultator/commit/f02a412f5cced96486e2664e4d6c76e6c7b3327e"
        },
        "date": 1758022986558,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.395730439472,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017508568025116293",
            "extra": "mean: 1.0622525338341717 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 297929.8420289122,
            "unit": "iter/sec",
            "range": "stddev: 5.656609323081724e-7",
            "extra": "mean: 3.3564949156820494 usec\nrounds: 106406"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156931.6486776932,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010438795651684322",
            "extra": "mean: 6.372200944971933 usec\nrounds: 108144"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 31738.548611173548,
            "unit": "iter/sec",
            "range": "stddev: 0.000004742242735225376",
            "extra": "mean: 31.50742689122055 usec\nrounds: 26358"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.48953159328113,
            "unit": "iter/sec",
            "range": "stddev: 0.000018031666213317102",
            "extra": "mean: 5.089329654823171 msec\nrounds: 197"
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
          "id": "959fdc47a3687b4a3f585a4ddf2b9727388b9ebe",
          "message": "Fix SonarCloud workflow with Java 17 and compatible scanner\n\n- Install Java 17 manually (GitHub Actions Java setup actions not resolving)\n- Use sonar-scanner-cli 4.6.2.2472 (compatible with Java 11/17)\n- Remove problematic GitHub actions, use direct CLI approach\n- Should resolve UnsupportedClassVersionError",
          "timestamp": "2025-09-16T13:41:26+02:00",
          "tree_id": "5a774cb345b1f12c5c4047bcb02c1eb2e9458c06",
          "url": "https://github.com/ericfunman/Consultator/commit/959fdc47a3687b4a3f585a4ddf2b9727388b9ebe"
        },
        "date": 1758023143273,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.1603942348239,
            "unit": "iter/sec",
            "range": "stddev: 0.00000852378670573912",
            "extra": "mean: 1.0636482946230448 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 282410.08093526453,
            "unit": "iter/sec",
            "range": "stddev: 0.000001012416791992433",
            "extra": "mean: 3.5409500846721724 usec\nrounds: 118681"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 148677.5602503628,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023044603591056297",
            "extra": "mean: 6.725964552526075 usec\nrounds: 23020"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32382.801254955582,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026350309133408376",
            "extra": "mean: 30.880589734248783 usec\nrounds: 27197"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.53308044160184,
            "unit": "iter/sec",
            "range": "stddev: 0.000014211497785316178",
            "extra": "mean: 5.088201934010502 msec\nrounds: 197"
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
          "id": "959fdc47a3687b4a3f585a4ddf2b9727388b9ebe",
          "message": "Fix SonarCloud workflow with Java 17 and compatible scanner\n\n- Install Java 17 manually (GitHub Actions Java setup actions not resolving)\n- Use sonar-scanner-cli 4.6.2.2472 (compatible with Java 11/17)\n- Remove problematic GitHub actions, use direct CLI approach\n- Should resolve UnsupportedClassVersionError",
          "timestamp": "2025-09-16T13:41:26+02:00",
          "tree_id": "5a774cb345b1f12c5c4047bcb02c1eb2e9458c06",
          "url": "https://github.com/ericfunman/Consultator/commit/959fdc47a3687b4a3f585a4ddf2b9727388b9ebe"
        },
        "date": 1758023151727,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4819165403715,
            "unit": "iter/sec",
            "range": "stddev: 0.000001799393974538849",
            "extra": "mean: 1.062155292025855 msec\nrounds: 928"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 287997.6546496835,
            "unit": "iter/sec",
            "range": "stddev: 4.94757865587865e-7",
            "extra": "mean: 3.4722504987632155 usec\nrounds: 110779"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157670.35278172066,
            "unit": "iter/sec",
            "range": "stddev: 7.297921435353207e-7",
            "extra": "mean: 6.342346435822359 usec\nrounds: 75558"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32006.83228949775,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017373402266448783",
            "extra": "mean: 31.243329266549292 usec\nrounds: 27704"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.44449367148974,
            "unit": "iter/sec",
            "range": "stddev: 0.000014874738575275456",
            "extra": "mean: 5.0904964619282245 msec\nrounds: 197"
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
          "id": "b52e54e34ba7e422d7a57feb5854884e34c30c45",
          "message": "Fix deprecated actions/cache@v2 in CI pipeline\n\n- Update actions/cache from v2 to v4 to avoid workflow failures\n- Resolves 'deprecated version' error in CI/CD pipeline\n- Maintains pip dependency caching functionality",
          "timestamp": "2025-09-16T13:45:56+02:00",
          "tree_id": "2ff9f6952fa4c70845af43de332b69fa4717c85c",
          "url": "https://github.com/ericfunman/Consultator/commit/b52e54e34ba7e422d7a57feb5854884e34c30c45"
        },
        "date": 1758023427116,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.447990619779,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015962228582712428",
            "extra": "mean: 1.0621935677420424 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289901.978746979,
            "unit": "iter/sec",
            "range": "stddev: 4.977877017021054e-7",
            "extra": "mean: 3.449441788297628 usec\nrounds: 56389"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159383.42973281172,
            "unit": "iter/sec",
            "range": "stddev: 7.566028312731926e-7",
            "extra": "mean: 6.274177947333588 usec\nrounds: 77197"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 31765.798888763995,
            "unit": "iter/sec",
            "range": "stddev: 0.000005380358648748861",
            "extra": "mean: 31.480398257942564 usec\nrounds: 27324"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.45857666522028,
            "unit": "iter/sec",
            "range": "stddev: 0.000015034778076208986",
            "extra": "mean: 5.090131553299772 msec\nrounds: 197"
          }
        ]
      }
    ]
  }
}