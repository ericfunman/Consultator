window.BENCHMARK_DATA = {
  "lastUpdate": 1757660079633,
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
      }
    ]
  }
}