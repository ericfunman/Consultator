window.BENCHMARK_DATA = {
  "lastUpdate": 1758096275631,
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
        "date": 1758023431313,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4448625138324,
            "unit": "iter/sec",
            "range": "stddev: 0.000001925650654475313",
            "extra": "mean: 1.0621970970554926 msec\nrounds: 917"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 288033.82460543216,
            "unit": "iter/sec",
            "range": "stddev: 6.733871300270718e-7",
            "extra": "mean: 3.471814469602195 usec\nrounds: 108144"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158912.49993467017,
            "unit": "iter/sec",
            "range": "stddev: 8.637841155092798e-7",
            "extra": "mean: 6.292771181694993 usec\nrounds: 78346"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33488.81685193986,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017692706545283186",
            "extra": "mean: 29.860714531097994 usec\nrounds: 27369"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.59601739961892,
            "unit": "iter/sec",
            "range": "stddev: 0.00001668655902549678",
            "extra": "mean: 5.086573030456203 msec\nrounds: 197"
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
          "id": "e68ad01e0db046894b910f3a98c995d3f3d3d39a",
          "message": "Fix pypdf version requirement for Python 3.8 compatibility\n\n- Change pypdf>=6.0.0 to pypdf>=5.9.0 (version 6.0.0 doesn't exist)\n- Latest available version is 5.9.0, compatible with Python 3.8+\n- Resolves CI/CD pipeline failure in test job for Python 3.8",
          "timestamp": "2025-09-16T13:47:48+02:00",
          "tree_id": "d52fac764e8cbeeff6c6256d94f962314b3acee6",
          "url": "https://github.com/ericfunman/Consultator/commit/e68ad01e0db046894b910f3a98c995d3f3d3d39a"
        },
        "date": 1758023526155,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.996974003521,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017394911501198601",
            "extra": "mean: 1.0627026734692329 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 294445.56246745115,
            "unit": "iter/sec",
            "range": "stddev: 5.596835750848101e-7",
            "extra": "mean: 3.396213519470319 usec\nrounds: 108969"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 154641.67720205718,
            "unit": "iter/sec",
            "range": "stddev: 8.661600518944056e-7",
            "extra": "mean: 6.466562042607601 usec\nrounds: 79663"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32973.40219087884,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016923388569326436",
            "extra": "mean: 30.327474071711702 usec\nrounds: 27711"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.49656244524562,
            "unit": "iter/sec",
            "range": "stddev: 0.000014196193296344333",
            "extra": "mean: 5.08914755329958 msec\nrounds: 197"
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
          "id": "e68ad01e0db046894b910f3a98c995d3f3d3d39a",
          "message": "Fix pypdf version requirement for Python 3.8 compatibility\n\n- Change pypdf>=6.0.0 to pypdf>=5.9.0 (version 6.0.0 doesn't exist)\n- Latest available version is 5.9.0, compatible with Python 3.8+\n- Resolves CI/CD pipeline failure in test job for Python 3.8",
          "timestamp": "2025-09-16T13:47:48+02:00",
          "tree_id": "d52fac764e8cbeeff6c6256d94f962314b3acee6",
          "url": "https://github.com/ericfunman/Consultator/commit/e68ad01e0db046894b910f3a98c995d3f3d3d39a"
        },
        "date": 1758023572596,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.5503632985317,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032628678564421834",
            "extra": "mean: 1.0632072869473752 msec\nrounds: 927"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 287143.7920272743,
            "unit": "iter/sec",
            "range": "stddev: 5.269307803349113e-7",
            "extra": "mean: 3.4825757260495296 usec\nrounds: 112524"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 145576.17811513107,
            "unit": "iter/sec",
            "range": "stddev: 0.000002701215616160802",
            "extra": "mean: 6.869255759751677 usec\nrounds: 75047"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33598.844591926194,
            "unit": "iter/sec",
            "range": "stddev: 0.000002742449671980148",
            "extra": "mean: 29.76292822403483 usec\nrounds: 25496"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 195.81465459083157,
            "unit": "iter/sec",
            "range": "stddev: 0.000025669311537701203",
            "extra": "mean: 5.106870076142003 msec\nrounds: 197"
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
          "id": "f8b4e9302e62a6b09bfb599bfeca3b22e5d8de11",
          "message": "Fix Black code formatting in consultant_profile.py\n\n- Reformatted long any() expressions to multiple lines for better readability\n- Changed single quotes to double quotes where appropriate\n- Made code compliant with Black formatting standards\n- Resolves CI/CD quality check failure",
          "timestamp": "2025-09-16T13:51:23+02:00",
          "tree_id": "1ee5a8e579f65bd83debf3812e9962cf26b91a3a",
          "url": "https://github.com/ericfunman/Consultator/commit/f8b4e9302e62a6b09bfb599bfeca3b22e5d8de11"
        },
        "date": 1758023748047,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2786809530279,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033905515947722854",
            "extra": "mean: 1.0623846266097496 msec\nrounds: 932"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 287150.3614808185,
            "unit": "iter/sec",
            "range": "stddev: 5.037510479235287e-7",
            "extra": "mean: 3.482496051347648 usec\nrounds: 119532"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 161465.9367349722,
            "unit": "iter/sec",
            "range": "stddev: 8.403434389731927e-7",
            "extra": "mean: 6.193256734027965 usec\nrounds: 77072"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32612.29028046441,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016794863106415371",
            "extra": "mean: 30.66328649107559 usec\nrounds: 27596"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.9449257300671,
            "unit": "iter/sec",
            "range": "stddev: 0.00001493884668807739",
            "extra": "mean: 5.0775616395956344 msec\nrounds: 197"
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
          "id": "f8b4e9302e62a6b09bfb599bfeca3b22e5d8de11",
          "message": "Fix Black code formatting in consultant_profile.py\n\n- Reformatted long any() expressions to multiple lines for better readability\n- Changed single quotes to double quotes where appropriate\n- Made code compliant with Black formatting standards\n- Resolves CI/CD quality check failure",
          "timestamp": "2025-09-16T13:51:23+02:00",
          "tree_id": "1ee5a8e579f65bd83debf3812e9962cf26b91a3a",
          "url": "https://github.com/ericfunman/Consultator/commit/f8b4e9302e62a6b09bfb599bfeca3b22e5d8de11"
        },
        "date": 1758023754254,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2853439021642,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014210606379575973",
            "extra": "mean: 1.0623771064515146 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 287887.2930350613,
            "unit": "iter/sec",
            "range": "stddev: 5.724552487731854e-7",
            "extra": "mean: 3.4735815862432378 usec\nrounds: 115381"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157177.0578913435,
            "unit": "iter/sec",
            "range": "stddev: 0.000001027444793826334",
            "extra": "mean: 6.362251676013048 usec\nrounds: 74433"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32925.12034751026,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017930803112170603",
            "extra": "mean: 30.371946691323735 usec\nrounds: 27050"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.5379416734525,
            "unit": "iter/sec",
            "range": "stddev: 0.000014312158159870435",
            "extra": "mean: 5.0880760808083485 msec\nrounds: 198"
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
          "id": "32f97c18c287b8684aeb7548e98942702851de4a",
          "message": "Fix Black code formatting in cache_service.py\n\n- Reformatted long function parameters to multiple lines\n- Changed single quotes to double quotes for consistency\n- Added proper spacing and line breaks\n- Made code compliant with Black formatting standards\n- Resolves CI/CD quality check failure",
          "timestamp": "2025-09-16T13:53:56+02:00",
          "tree_id": "9b04aa998f76c7bea69c30fe0526c49affbb12b3",
          "url": "https://github.com/ericfunman/Consultator/commit/32f97c18c287b8684aeb7548e98942702851de4a"
        },
        "date": 1758023903480,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2005993871869,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023164463700634824",
            "extra": "mean: 1.0624727615463667 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 295836.8846533883,
            "unit": "iter/sec",
            "range": "stddev: 4.980465579320473e-7",
            "extra": "mean: 3.3802411121643305 usec\nrounds: 106747"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157892.85827481677,
            "unit": "iter/sec",
            "range": "stddev: 7.35939025580859e-7",
            "extra": "mean: 6.333408685651082 usec\nrounds: 77737"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33097.755704460775,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017473451602461566",
            "extra": "mean: 30.21352894526393 usec\nrounds: 27362"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.50034638625203,
            "unit": "iter/sec",
            "range": "stddev: 0.000017331286006600738",
            "extra": "mean: 5.089049553298722 msec\nrounds: 197"
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
          "id": "32f97c18c287b8684aeb7548e98942702851de4a",
          "message": "Fix Black code formatting in cache_service.py\n\n- Reformatted long function parameters to multiple lines\n- Changed single quotes to double quotes for consistency\n- Added proper spacing and line breaks\n- Made code compliant with Black formatting standards\n- Resolves CI/CD quality check failure",
          "timestamp": "2025-09-16T13:53:56+02:00",
          "tree_id": "9b04aa998f76c7bea69c30fe0526c49affbb12b3",
          "url": "https://github.com/ericfunman/Consultator/commit/32f97c18c287b8684aeb7548e98942702851de4a"
        },
        "date": 1758023910517,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.0325208550062,
            "unit": "iter/sec",
            "range": "stddev: 0.000004299817157226368",
            "extra": "mean: 1.0626625306120314 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 287574.4371794108,
            "unit": "iter/sec",
            "range": "stddev: 5.233660643599232e-7",
            "extra": "mean: 3.4773605394422598 usec\nrounds: 119532"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 160167.59902547483,
            "unit": "iter/sec",
            "range": "stddev: 7.036755068982168e-7",
            "extra": "mean: 6.243460013663243 usec\nrounds: 78902"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33652.43197068822,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017133793465958909",
            "extra": "mean: 29.715534403903266 usec\nrounds: 27773"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.5739093427267,
            "unit": "iter/sec",
            "range": "stddev: 0.000013592377793022963",
            "extra": "mean: 5.0871451015226015 msec\nrounds: 197"
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
          "id": "2871e552e965e4b5ab36e1f12a5ff48eb858a00d",
          "message": "Fix Black code formatting in multiple files\n\n- Reformatted practices.py: improved column layout formatting\n- Reformatted consultant_service.py: fixed parameter alignment and quotes\n- Reformatted enhanced_ui.py: standardized code formatting\n- All files now compliant with Black formatting standards\n- Resolves CI/CD quality check failures",
          "timestamp": "2025-09-16T13:58:12+02:00",
          "tree_id": "abe7f53e03f281ccf0a30e2b11b27e704a6536c4",
          "url": "https://github.com/ericfunman/Consultator/commit/2871e552e965e4b5ab36e1f12a5ff48eb858a00d"
        },
        "date": 1758024146626,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 939.8983097138512,
            "unit": "iter/sec",
            "range": "stddev: 0.000007399326637657513",
            "extra": "mean: 1.0639448860211767 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 287909.84109169693,
            "unit": "iter/sec",
            "range": "stddev: 5.173002641852515e-7",
            "extra": "mean: 3.4733095479063816 usec\nrounds: 117565"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 155302.11112368395,
            "unit": "iter/sec",
            "range": "stddev: 7.796464774389025e-7",
            "extra": "mean: 6.439062500596604 usec\nrounds: 107551"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33361.26930470751,
            "unit": "iter/sec",
            "range": "stddev: 0.000001639432906217911",
            "extra": "mean: 29.974878679418023 usec\nrounds: 27959"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.52231939860718,
            "unit": "iter/sec",
            "range": "stddev: 0.000015802936299273792",
            "extra": "mean: 5.088480550505285 msec\nrounds: 198"
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
          "id": "2871e552e965e4b5ab36e1f12a5ff48eb858a00d",
          "message": "Fix Black code formatting in multiple files\n\n- Reformatted practices.py: improved column layout formatting\n- Reformatted consultant_service.py: fixed parameter alignment and quotes\n- Reformatted enhanced_ui.py: standardized code formatting\n- All files now compliant with Black formatting standards\n- Resolves CI/CD quality check failures",
          "timestamp": "2025-09-16T13:58:12+02:00",
          "tree_id": "abe7f53e03f281ccf0a30e2b11b27e704a6536c4",
          "url": "https://github.com/ericfunman/Consultator/commit/2871e552e965e4b5ab36e1f12a5ff48eb858a00d"
        },
        "date": 1758024158186,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4508128574037,
            "unit": "iter/sec",
            "range": "stddev: 0.000002418254532103492",
            "extra": "mean: 1.0621903835473818 msec\nrounds: 936"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289385.51691741793,
            "unit": "iter/sec",
            "range": "stddev: 5.259311286053964e-7",
            "extra": "mean: 3.455597953388146 usec\nrounds: 123518"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157744.34681731573,
            "unit": "iter/sec",
            "range": "stddev: 7.088497389582595e-7",
            "extra": "mean: 6.339371395401595 usec\nrounds: 78162"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32502.412240060086,
            "unit": "iter/sec",
            "range": "stddev: 0.000004692499991633832",
            "extra": "mean: 30.766947161154807 usec\nrounds: 27688"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.5670972151052,
            "unit": "iter/sec",
            "range": "stddev: 0.000014051164364013537",
            "extra": "mean: 5.08732139899126 msec\nrounds: 198"
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
          "id": "b3f2b6a142125a82ec7d9e5c5ffef42087957a65",
          "message": "fix: Corriger les erreurs de syntaxe dans consultants.py et appliquer le formatage Black\n\n- Correction des f-strings malformées dans show_existing_documents()\n- Correction des f-strings dans les fonctions de nommage de documents\n- Application du formatage Black pour respecter les standards de code\n- Résolution des erreurs de syntaxe bloquant le CI/CD",
          "timestamp": "2025-09-16T14:04:21+02:00",
          "tree_id": "94c4b9ea43382f189cd32b3c6f0da050fcbd3fe8",
          "url": "https://github.com/ericfunman/Consultator/commit/b3f2b6a142125a82ec7d9e5c5ffef42087957a65"
        },
        "date": 1758024642753,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3694793167298,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018937414997143103",
            "extra": "mean: 1.0622821559137712 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 290041.9836763491,
            "unit": "iter/sec",
            "range": "stddev: 5.402575492460944e-7",
            "extra": "mean: 3.4477767229584115 usec\nrounds: 114078"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 163196.21048403688,
            "unit": "iter/sec",
            "range": "stddev: 7.313346022402751e-7",
            "extra": "mean: 6.12759326355691 usec\nrounds: 79656"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32331.158133233446,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019015898409163462",
            "extra": "mean: 30.929915837815052 usec\nrounds: 27649"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.49165265650024,
            "unit": "iter/sec",
            "range": "stddev: 0.000014589180576442629",
            "extra": "mean: 5.089274717171649 msec\nrounds: 198"
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
          "id": "b3f2b6a142125a82ec7d9e5c5ffef42087957a65",
          "message": "fix: Corriger les erreurs de syntaxe dans consultants.py et appliquer le formatage Black\n\n- Correction des f-strings malformées dans show_existing_documents()\n- Correction des f-strings dans les fonctions de nommage de documents\n- Application du formatage Black pour respecter les standards de code\n- Résolution des erreurs de syntaxe bloquant le CI/CD",
          "timestamp": "2025-09-16T14:04:21+02:00",
          "tree_id": "94c4b9ea43382f189cd32b3c6f0da050fcbd3fe8",
          "url": "https://github.com/ericfunman/Consultator/commit/b3f2b6a142125a82ec7d9e5c5ffef42087957a65"
        },
        "date": 1758024644522,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.1515847493955,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036416893487821758",
            "extra": "mean: 1.0625280945218556 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 293178.66361581103,
            "unit": "iter/sec",
            "range": "stddev: 5.270260604079111e-7",
            "extra": "mean: 3.4108894135298535 usec\nrounds: 114996"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157304.6920196725,
            "unit": "iter/sec",
            "range": "stddev: 7.260174126784777e-7",
            "extra": "mean: 6.357089462245284 usec\nrounds: 75965"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33256.44271898895,
            "unit": "iter/sec",
            "range": "stddev: 0.000001832097013367718",
            "extra": "mean: 30.06936155047679 usec\nrounds: 26934"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.52711076679196,
            "unit": "iter/sec",
            "range": "stddev: 0.000014026273362568315",
            "extra": "mean: 5.0883564923856515 msec\nrounds: 197"
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
          "id": "28fe37d31f62e5e3564b55ba3c790e0d57ec1689",
          "message": "fix: Corriger le formatage des imports avec isort\n\n- Tri et formatage corrects des imports dans cache_service.py\n- Tri et formatage corrects des imports dans enhanced_ui.py\n- Tri et formatage corrects des imports dans consultants.py\n- Respect des standards de formatage pour éviter les erreurs CI/CD",
          "timestamp": "2025-09-16T14:08:17+02:00",
          "tree_id": "ab462b5ed69321c4e247ec5d6531997cce6b31af",
          "url": "https://github.com/ericfunman/Consultator/commit/28fe37d31f62e5e3564b55ba3c790e0d57ec1689"
        },
        "date": 1758024768668,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.7039658562552,
            "unit": "iter/sec",
            "range": "stddev: 0.000002087658694652617",
            "extra": "mean: 1.0619048408601939 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 288587.1037424064,
            "unit": "iter/sec",
            "range": "stddev: 5.262040257827774e-7",
            "extra": "mean: 3.4651583076026937 usec\nrounds: 118554"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158368.42067735668,
            "unit": "iter/sec",
            "range": "stddev: 7.351144418828512e-7",
            "extra": "mean: 6.314390177807581 usec\nrounds: 79656"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32930.884577827695,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018257725346993731",
            "extra": "mean: 30.366630378137433 usec\nrounds: 27612"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.70861022452087,
            "unit": "iter/sec",
            "range": "stddev: 0.000014784913591849363",
            "extra": "mean: 5.083661558376178 msec\nrounds: 197"
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
          "id": "28fe37d31f62e5e3564b55ba3c790e0d57ec1689",
          "message": "fix: Corriger le formatage des imports avec isort\n\n- Tri et formatage corrects des imports dans cache_service.py\n- Tri et formatage corrects des imports dans enhanced_ui.py\n- Tri et formatage corrects des imports dans consultants.py\n- Respect des standards de formatage pour éviter les erreurs CI/CD",
          "timestamp": "2025-09-16T14:08:17+02:00",
          "tree_id": "ab462b5ed69321c4e247ec5d6531997cce6b31af",
          "url": "https://github.com/ericfunman/Consultator/commit/28fe37d31f62e5e3564b55ba3c790e0d57ec1689"
        },
        "date": 1758024841117,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.9490364063531,
            "unit": "iter/sec",
            "range": "stddev: 0.000004297674870288544",
            "extra": "mean: 1.0627568139281727 msec\nrounds: 919"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 283640.7104359156,
            "unit": "iter/sec",
            "range": "stddev: 6.348634923015513e-7",
            "extra": "mean: 3.5255869951218974 usec\nrounds: 116064"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 160088.9009845731,
            "unit": "iter/sec",
            "range": "stddev: 7.124216930329392e-7",
            "extra": "mean: 6.2465292337559655 usec\nrounds: 36020"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33564.44840084227,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017232415325001907",
            "extra": "mean: 29.79342869149924 usec\nrounds: 27339"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.50982549825264,
            "unit": "iter/sec",
            "range": "stddev: 0.000014008085559301247",
            "extra": "mean: 5.088804071066116 msec\nrounds: 197"
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
          "id": "729b9e69247b2a0b8930ada64e87e9d41c2d8577",
          "message": "fix: Mettre à jour le scanner SonarQube vers la version 5.0.1.3006\n\n- Changement de sonar-scanner-cli-4.6.2.2472 vers sonar-scanner-cli-5.0.1.3006\n- Version plus récente compatible avec Java 17\n- Résout l'erreur UnsupportedClassVersionError dans SonarCloud",
          "timestamp": "2025-09-16T14:15:59+02:00",
          "tree_id": "042d610edc74da3ce1eec29b7eda1c76dca54d51",
          "url": "https://github.com/ericfunman/Consultator/commit/729b9e69247b2a0b8930ada64e87e9d41c2d8577"
        },
        "date": 1758025224678,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.7395983796257,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015440975800380535",
            "extra": "mean: 1.0618646616544722 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 283197.52217716514,
            "unit": "iter/sec",
            "range": "stddev: 6.383926886955079e-7",
            "extra": "mean: 3.5311043412816705 usec\nrounds: 112918"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156657.07999857367,
            "unit": "iter/sec",
            "range": "stddev: 7.009568835208699e-7",
            "extra": "mean: 6.383369331338901 usec\nrounds: 76430"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33173.01797630016,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017532478951109984",
            "extra": "mean: 30.144981102244937 usec\nrounds: 26511"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.56478178877936,
            "unit": "iter/sec",
            "range": "stddev: 0.000015107463851342108",
            "extra": "mean: 5.08738132487314 msec\nrounds: 197"
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
          "id": "729b9e69247b2a0b8930ada64e87e9d41c2d8577",
          "message": "fix: Mettre à jour le scanner SonarQube vers la version 5.0.1.3006\n\n- Changement de sonar-scanner-cli-4.6.2.2472 vers sonar-scanner-cli-5.0.1.3006\n- Version plus récente compatible avec Java 17\n- Résout l'erreur UnsupportedClassVersionError dans SonarCloud",
          "timestamp": "2025-09-16T14:15:59+02:00",
          "tree_id": "042d610edc74da3ce1eec29b7eda1c76dca54d51",
          "url": "https://github.com/ericfunman/Consultator/commit/729b9e69247b2a0b8930ada64e87e9d41c2d8577"
        },
        "date": 1758025233542,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.392697712423,
            "unit": "iter/sec",
            "range": "stddev: 0.000004302276804635859",
            "extra": "mean: 1.062255955915095 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 292489.4269808294,
            "unit": "iter/sec",
            "range": "stddev: 5.143414679463597e-7",
            "extra": "mean: 3.4189270030110968 usec\nrounds: 115128"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156642.9776145633,
            "unit": "iter/sec",
            "range": "stddev: 9.887089390067954e-7",
            "extra": "mean: 6.383944018611586 usec\nrounds: 75615"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33140.27161488365,
            "unit": "iter/sec",
            "range": "stddev: 0.000001951792033169293",
            "extra": "mean: 30.174767775617422 usec\nrounds: 26539"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.55269484517444,
            "unit": "iter/sec",
            "range": "stddev: 0.000016617792665507427",
            "extra": "mean: 5.087694171721762 msec\nrounds: 198"
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
          "id": "4ba1eb3e71c9d26ccc2cbff984c721ac987941bc",
          "message": "fix: Corriger les erreurs de syntaxe dans les f-strings\n\n- Correction f-string malformée dans chatbot_service.py (ligne 581)\n- Correction f-string malformée dans consultant_forms.py (ligne 222)\n- Résolution des erreurs SyntaxError bloquant les tests CI/CD",
          "timestamp": "2025-09-16T14:21:29+02:00",
          "tree_id": "f57820eb8b4edeeb4de7417272d34cd1b90765bf",
          "url": "https://github.com/ericfunman/Consultator/commit/4ba1eb3e71c9d26ccc2cbff984c721ac987941bc"
        },
        "date": 1758025622724,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.5654118829929,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011422832079368024",
            "extra": "mean: 1.0620611031156577 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 291345.6800657831,
            "unit": "iter/sec",
            "range": "stddev: 5.363856804949665e-7",
            "extra": "mean: 3.4323488159296187 usec\nrounds: 113676"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157126.89647929638,
            "unit": "iter/sec",
            "range": "stddev: 6.910580520177497e-7",
            "extra": "mean: 6.364282770211551 usec\nrounds: 75793"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33106.997690222044,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021724990848166283",
            "extra": "mean: 30.205094685929314 usec\nrounds: 27079"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.57714094637242,
            "unit": "iter/sec",
            "range": "stddev: 0.000013494830881904693",
            "extra": "mean: 5.087061472080352 msec\nrounds: 197"
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
          "id": "4ba1eb3e71c9d26ccc2cbff984c721ac987941bc",
          "message": "fix: Corriger les erreurs de syntaxe dans les f-strings\n\n- Correction f-string malformée dans chatbot_service.py (ligne 581)\n- Correction f-string malformée dans consultant_forms.py (ligne 222)\n- Résolution des erreurs SyntaxError bloquant les tests CI/CD",
          "timestamp": "2025-09-16T14:21:29+02:00",
          "tree_id": "f57820eb8b4edeeb4de7417272d34cd1b90765bf",
          "url": "https://github.com/ericfunman/Consultator/commit/4ba1eb3e71c9d26ccc2cbff984c721ac987941bc"
        },
        "date": 1758025633926,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.725202088216,
            "unit": "iter/sec",
            "range": "stddev: 0.000004905089893128242",
            "extra": "mean: 1.0630096842098056 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 297403.5504959548,
            "unit": "iter/sec",
            "range": "stddev: 8.981172890670264e-7",
            "extra": "mean: 3.362434639170865 usec\nrounds: 117578"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158466.5439191563,
            "unit": "iter/sec",
            "range": "stddev: 9.579412884755421e-7",
            "extra": "mean: 6.310480277213356 usec\nrounds: 111521"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32691.65741899275,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018875867739349722",
            "extra": "mean: 30.588843728034227 usec\nrounds: 26889"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.58893450381967,
            "unit": "iter/sec",
            "range": "stddev: 0.00001586140673977819",
            "extra": "mean: 5.0867562944168165 msec\nrounds: 197"
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
          "id": "5a40c0a074c2b06b9d62b110b6f1356570c1ea12",
          "message": "fix: Corriger les erreurs de syntaxe f-string et résoudre les problèmes de tests CI/CD\n\n- Corriger les f-strings malformées dans 4 fichiers :\n  * app/services/chatbot_service.py (ligne 597)\n  * app/pages_modules/consultant_forms.py (ligne 222)\n  * app/pages_modules/consultant_skills.py (ligne 151)\n  * app/pages_modules/consultants.py (ligne 1707)\n\n- Supprimer les fichiers de test corrompus qui empêchaient pytest de fonctionner\n- Modifier pytest.ini pour améliorer la configuration des tests\n\nRésout les erreurs de syntaxe qui bloquaient le pipeline CI/CD GitHub Actions.",
          "timestamp": "2025-09-16T14:42:42+02:00",
          "tree_id": "7d2920c2e307bfa5142fc80366565e13fc5bf003",
          "url": "https://github.com/ericfunman/Consultator/commit/5a40c0a074c2b06b9d62b110b6f1356570c1ea12"
        },
        "date": 1758026830988,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3568859965833,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015053211458772385",
            "extra": "mean: 1.0622963669526178 msec\nrounds: 932"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 295379.760114449,
            "unit": "iter/sec",
            "range": "stddev: 6.172686266519632e-7",
            "extra": "mean: 3.385472314056102 usec\nrounds: 123077"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156863.8513383704,
            "unit": "iter/sec",
            "range": "stddev: 7.696939953142298e-7",
            "extra": "mean: 6.3749550420185965 usec\nrounds: 106633"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33322.756162802434,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017727590526884206",
            "extra": "mean: 30.009522475103104 usec\nrounds: 27764"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.50953355133777,
            "unit": "iter/sec",
            "range": "stddev: 0.000014780890688316915",
            "extra": "mean: 5.088811631313306 msec\nrounds: 198"
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
          "id": "5a40c0a074c2b06b9d62b110b6f1356570c1ea12",
          "message": "fix: Corriger les erreurs de syntaxe f-string et résoudre les problèmes de tests CI/CD\n\n- Corriger les f-strings malformées dans 4 fichiers :\n  * app/services/chatbot_service.py (ligne 597)\n  * app/pages_modules/consultant_forms.py (ligne 222)\n  * app/pages_modules/consultant_skills.py (ligne 151)\n  * app/pages_modules/consultants.py (ligne 1707)\n\n- Supprimer les fichiers de test corrompus qui empêchaient pytest de fonctionner\n- Modifier pytest.ini pour améliorer la configuration des tests\n\nRésout les erreurs de syntaxe qui bloquaient le pipeline CI/CD GitHub Actions.",
          "timestamp": "2025-09-16T14:42:42+02:00",
          "tree_id": "7d2920c2e307bfa5142fc80366565e13fc5bf003",
          "url": "https://github.com/ericfunman/Consultator/commit/5a40c0a074c2b06b9d62b110b6f1356570c1ea12"
        },
        "date": 1758026833316,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4549056832724,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029993819545922963",
            "extra": "mean: 1.062185765843174 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 296811.5679938793,
            "unit": "iter/sec",
            "range": "stddev: 5.327456679188747e-7",
            "extra": "mean: 3.369140922501449 usec\nrounds: 106406"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158687.75585428366,
            "unit": "iter/sec",
            "range": "stddev: 7.1777901245327e-7",
            "extra": "mean: 6.301683419849091 usec\nrounds: 78413"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33125.157227983924,
            "unit": "iter/sec",
            "range": "stddev: 0.000002364697078694983",
            "extra": "mean: 30.188535955240877 usec\nrounds: 27131"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.62777850298744,
            "unit": "iter/sec",
            "range": "stddev: 0.000015107107070130344",
            "extra": "mean: 5.08575140101482 msec\nrounds: 197"
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
          "id": "7149c2f69ce0da1ed971408bd95e7d73a7a1026d",
          "message": "fix: Corriger les erreurs de syntaxe f-string et résoudre les problèmes de tests CI/CD\n\n- Correction de la f-string malformée dans chatbot_service.py ligne 599\n- Désactivation de l'assertion rewriting de pytest pour éviter la corruption des fichiers de test\n- Suppression des fichiers de test corrompus test_skill_categories.py et test_technologies_referentiel.py\n- Nettoyage du cache pytest\n- Tests passent maintenant : 469 tests réussis",
          "timestamp": "2025-09-16T15:18:59+02:00",
          "tree_id": "661abd85a011b84d73e792cbb377ee5977818f7c",
          "url": "https://github.com/ericfunman/Consultator/commit/7149c2f69ce0da1ed971408bd95e7d73a7a1026d"
        },
        "date": 1758029016740,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.9821686438089,
            "unit": "iter/sec",
            "range": "stddev: 0.000013603730150267586",
            "extra": "mean: 1.0627193939724178 msec\nrounds: 929"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 255821.99044445704,
            "unit": "iter/sec",
            "range": "stddev: 5.98476363455934e-7",
            "extra": "mean: 3.908968100289704 usec\nrounds: 108496"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159734.78452102584,
            "unit": "iter/sec",
            "range": "stddev: 8.264884559534768e-7",
            "extra": "mean: 6.260377180828578 usec\nrounds: 61729"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32380.517182991956,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018904419397036545",
            "extra": "mean: 30.88276800363323 usec\nrounds: 28022"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.7200502537706,
            "unit": "iter/sec",
            "range": "stddev: 0.000019176409912200684",
            "extra": "mean: 5.083365923859775 msec\nrounds: 197"
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
          "id": "7149c2f69ce0da1ed971408bd95e7d73a7a1026d",
          "message": "fix: Corriger les erreurs de syntaxe f-string et résoudre les problèmes de tests CI/CD\n\n- Correction de la f-string malformée dans chatbot_service.py ligne 599\n- Désactivation de l'assertion rewriting de pytest pour éviter la corruption des fichiers de test\n- Suppression des fichiers de test corrompus test_skill_categories.py et test_technologies_referentiel.py\n- Nettoyage du cache pytest\n- Tests passent maintenant : 469 tests réussis",
          "timestamp": "2025-09-16T15:18:59+02:00",
          "tree_id": "661abd85a011b84d73e792cbb377ee5977818f7c",
          "url": "https://github.com/ericfunman/Consultator/commit/7149c2f69ce0da1ed971408bd95e7d73a7a1026d"
        },
        "date": 1758029018183,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.1820959625975,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013950435467220579",
            "extra": "mean: 1.0624936495176804 msec\nrounds: 933"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 282461.9685909105,
            "unit": "iter/sec",
            "range": "stddev: 5.402415112329997e-7",
            "extra": "mean: 3.5402996197633225 usec\nrounds: 127812"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158457.363995451,
            "unit": "iter/sec",
            "range": "stddev: 7.642692923148837e-7",
            "extra": "mean: 6.310845862794411 usec\nrounds: 79027"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32903.65026039091,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018165880232275139",
            "extra": "mean: 30.391764806830263 usec\nrounds: 27960"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.39923594835176,
            "unit": "iter/sec",
            "range": "stddev: 0.000015706515821524496",
            "extra": "mean: 5.091669502538063 msec\nrounds: 197"
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
          "id": "bef10f5c135e0580b109c70888413328c9df2cce",
          "message": "fix: Corriger les erreurs de syntaxe f-string restantes\n\n- Correction de la f-string malformée dans chatbot_service.py ligne 675\n- Correction de la f-string malformée dans consultant_skills.py ligne 244\n- Correction de la f-string malformée dans consultants.py ligne 2851\n- Suppression définitive des fichiers de test corrompus\n- Nettoyage complet des caches pytest\n- Tests passent maintenant : 469 tests réussis\n\nToutes les erreurs de syntaxe f-string ont été résolues.",
          "timestamp": "2025-09-16T15:33:47+02:00",
          "tree_id": "c2b477ffec1c972d5f0a85bef066ba7dedd0e5d7",
          "url": "https://github.com/ericfunman/Consultator/commit/bef10f5c135e0580b109c70888413328c9df2cce"
        },
        "date": 1758029946518,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.7820909275821,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032548530229146876",
            "extra": "mean: 1.062945404300831 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 294954.248607223,
            "unit": "iter/sec",
            "range": "stddev: 4.981932899209498e-7",
            "extra": "mean: 3.3903563170288624 usec\nrounds: 103972"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158291.54086323178,
            "unit": "iter/sec",
            "range": "stddev: 8.9213019772945e-7",
            "extra": "mean: 6.317456981886527 usec\nrounds: 109326"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 31523.124517986744,
            "unit": "iter/sec",
            "range": "stddev: 0.000006315009292251125",
            "extra": "mean: 31.7227437092859 usec\nrounds: 26825"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.52156902630722,
            "unit": "iter/sec",
            "range": "stddev: 0.00002155172857774369",
            "extra": "mean: 5.088499979695031 msec\nrounds: 197"
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
          "id": "bef10f5c135e0580b109c70888413328c9df2cce",
          "message": "fix: Corriger les erreurs de syntaxe f-string restantes\n\n- Correction de la f-string malformée dans chatbot_service.py ligne 675\n- Correction de la f-string malformée dans consultant_skills.py ligne 244\n- Correction de la f-string malformée dans consultants.py ligne 2851\n- Suppression définitive des fichiers de test corrompus\n- Nettoyage complet des caches pytest\n- Tests passent maintenant : 469 tests réussis\n\nToutes les erreurs de syntaxe f-string ont été résolues.",
          "timestamp": "2025-09-16T15:33:47+02:00",
          "tree_id": "c2b477ffec1c972d5f0a85bef066ba7dedd0e5d7",
          "url": "https://github.com/ericfunman/Consultator/commit/bef10f5c135e0580b109c70888413328c9df2cce"
        },
        "date": 1758029961767,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.5229510349941,
            "unit": "iter/sec",
            "range": "stddev: 0.000002395338932775085",
            "extra": "mean: 1.062108999999122 msec\nrounds: 928"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 260485.65701443297,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011611471020910848",
            "extra": "mean: 3.8389829653637784 usec\nrounds: 117703"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157193.79724751163,
            "unit": "iter/sec",
            "range": "stddev: 0.000001056080991239604",
            "extra": "mean: 6.361574168384242 usec\nrounds: 75558"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33137.71929010967,
            "unit": "iter/sec",
            "range": "stddev: 0.000003049514898899802",
            "extra": "mean: 30.177091888712493 usec\nrounds: 27294"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.47203504254998,
            "unit": "iter/sec",
            "range": "stddev: 0.00001474682845972898",
            "extra": "mean: 5.089782878176173 msec\nrounds: 197"
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
          "id": "910f95fddaf9174d01d67e3ef236726564b58344",
          "message": " Correction finale des erreurs de syntaxe f-strings - Pipeline CI/CD réparé",
          "timestamp": "2025-09-16T15:46:04+02:00",
          "tree_id": "78927ba7813b52564720bd020f2db7117e766d1c",
          "url": "https://github.com/ericfunman/Consultator/commit/910f95fddaf9174d01d67e3ef236726564b58344"
        },
        "date": 1758030713936,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.754296152412,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016988416207554013",
            "extra": "mean: 1.0618480893429996 msec\nrounds: 929"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 288156.7206285812,
            "unit": "iter/sec",
            "range": "stddev: 5.168463225285978e-7",
            "extra": "mean: 3.470333774685572 usec\nrounds: 113289"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 145299.8334687096,
            "unit": "iter/sec",
            "range": "stddev: 7.409665387967022e-7",
            "extra": "mean: 6.882320344953118 usec\nrounds: 71654"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33119.662541114216,
            "unit": "iter/sec",
            "range": "stddev: 0.000001800852041307326",
            "extra": "mean: 30.19354435627525 usec\nrounds: 27065"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.91213524540063,
            "unit": "iter/sec",
            "range": "stddev: 0.00001660294551863036",
            "extra": "mean: 5.078407172588706 msec\nrounds: 197"
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
          "id": "910f95fddaf9174d01d67e3ef236726564b58344",
          "message": " Correction finale des erreurs de syntaxe f-strings - Pipeline CI/CD réparé",
          "timestamp": "2025-09-16T15:46:04+02:00",
          "tree_id": "78927ba7813b52564720bd020f2db7117e766d1c",
          "url": "https://github.com/ericfunman/Consultator/commit/910f95fddaf9174d01d67e3ef236726564b58344"
        },
        "date": 1758030716222,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.0376467550025,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015515290427225144",
            "extra": "mean: 1.0626567422125124 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 294043.4000159543,
            "unit": "iter/sec",
            "range": "stddev: 5.252898848810053e-7",
            "extra": "mean: 3.4008585125384267 usec\nrounds: 127976"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158998.4273584226,
            "unit": "iter/sec",
            "range": "stddev: 8.16498457359194e-7",
            "extra": "mean: 6.289370383178365 usec\nrounds: 81143"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33237.94807222605,
            "unit": "iter/sec",
            "range": "stddev: 0.00000393341978066761",
            "extra": "mean: 30.08609309536799 usec\nrounds: 19668"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.56505990225952,
            "unit": "iter/sec",
            "range": "stddev: 0.000014573536992967905",
            "extra": "mean: 5.087374126903542 msec\nrounds: 197"
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
          "id": "d7fdeef35776f3d8f908e7616ae232c0b576c7fd",
          "message": " Correction critique f-strings multi-lignes - Fix pipeline CI/CD Linux\n\n Corrections appliquées :\n- chatbot_service.py ligne 686 : Consolidation f-string date_entree_societe\n- consultants.py ligne 3177 : Consolidation f-string compteur compétences\n\n Problème résolu : Différences de parsing f-strings entre Windows/Linux\n Pipeline CI/CD maintenant compatible toutes plateformes",
          "timestamp": "2025-09-16T15:51:36+02:00",
          "tree_id": "7865652782e7c98a9413c67cff6cc0c89cb6f3ba",
          "url": "https://github.com/ericfunman/Consultator/commit/d7fdeef35776f3d8f908e7616ae232c0b576c7fd"
        },
        "date": 1758030969893,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2939267703055,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025650430118081963",
            "extra": "mean: 1.0623674195276307 msec\nrounds: 932"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289175.40730476985,
            "unit": "iter/sec",
            "range": "stddev: 5.354959450496897e-7",
            "extra": "mean: 3.4581087282642704 usec\nrounds: 107562"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159205.0008715658,
            "unit": "iter/sec",
            "range": "stddev: 7.067091285815274e-7",
            "extra": "mean: 6.281209726613564 usec\nrounds: 108732"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 31572.585735233894,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016957008527435895",
            "extra": "mean: 31.67304725643789 usec\nrounds: 26811"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.48874199131302,
            "unit": "iter/sec",
            "range": "stddev: 0.000014436817265753682",
            "extra": "mean: 5.089350106604128 msec\nrounds: 197"
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
          "id": "d7fdeef35776f3d8f908e7616ae232c0b576c7fd",
          "message": " Correction critique f-strings multi-lignes - Fix pipeline CI/CD Linux\n\n Corrections appliquées :\n- chatbot_service.py ligne 686 : Consolidation f-string date_entree_societe\n- consultants.py ligne 3177 : Consolidation f-string compteur compétences\n\n Problème résolu : Différences de parsing f-strings entre Windows/Linux\n Pipeline CI/CD maintenant compatible toutes plateformes",
          "timestamp": "2025-09-16T15:51:36+02:00",
          "tree_id": "7865652782e7c98a9413c67cff6cc0c89cb6f3ba",
          "url": "https://github.com/ericfunman/Consultator/commit/d7fdeef35776f3d8f908e7616ae232c0b576c7fd"
        },
        "date": 1758030982982,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4155398784794,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020643293185029492",
            "extra": "mean: 1.0622301817209039 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 300509.0237283484,
            "unit": "iter/sec",
            "range": "stddev: 5.774488141782118e-7",
            "extra": "mean: 3.3276870943615044 usec\nrounds: 114469"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159916.4248994493,
            "unit": "iter/sec",
            "range": "stddev: 6.984358727925313e-7",
            "extra": "mean: 6.253266358529277 usec\nrounds: 81150"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32203.514021247527,
            "unit": "iter/sec",
            "range": "stddev: 0.000003986349349942002",
            "extra": "mean: 31.05251182651095 usec\nrounds: 27650"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.21040889527296,
            "unit": "iter/sec",
            "range": "stddev: 0.0000093192089950858",
            "extra": "mean: 5.096569573603756 msec\nrounds: 197"
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
          "id": "e94eae001ded5504b26c9af8ae3996bd6836268c",
          "message": " Correction massive f-strings multi-lignes - Compatibilité Python 3.10\n\n Script automatique appliqué sur 11 fichiers :\n- business_managers.py\n- consultants.py\n- consultants_clean.py\n- consultants_final.py\n- consultants_optimized.py\n- consultant_cv.py\n- practices_optimized.py\n- chatbot_service.py\n- document_analyzer.py\n- document_analyzer_clean.py\n- simple_analyzer.py\n\n Objectif : Résoudre ALL les erreurs de syntaxe f-strings pour Python 3.10/Linux\n Pipeline CI/CD maintenant 100% compatible",
          "timestamp": "2025-09-16T15:57:31+02:00",
          "tree_id": "f943cdd85baec08d116cbb903f0313db44ef58cf",
          "url": "https://github.com/ericfunman/Consultator/commit/e94eae001ded5504b26c9af8ae3996bd6836268c"
        },
        "date": 1758031326056,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.7573495621573,
            "unit": "iter/sec",
            "range": "stddev: 0.0000045431177842988365",
            "extra": "mean: 1.0629733591402877 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 290765.18437678384,
            "unit": "iter/sec",
            "range": "stddev: 5.506349010836704e-7",
            "extra": "mean: 3.439201299644474 usec\nrounds: 115261"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158429.29983943544,
            "unit": "iter/sec",
            "range": "stddev: 7.593851422912622e-7",
            "extra": "mean: 6.311963765625915 usec\nrounds: 79593"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33911.35285452582,
            "unit": "iter/sec",
            "range": "stddev: 0.000001668067641854413",
            "extra": "mean: 29.48864954724269 usec\nrounds: 15129"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.92763626758364,
            "unit": "iter/sec",
            "range": "stddev: 0.00001529234259869825",
            "extra": "mean: 5.078007429293511 msec\nrounds: 198"
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
          "id": "e94eae001ded5504b26c9af8ae3996bd6836268c",
          "message": " Correction massive f-strings multi-lignes - Compatibilité Python 3.10\n\n Script automatique appliqué sur 11 fichiers :\n- business_managers.py\n- consultants.py\n- consultants_clean.py\n- consultants_final.py\n- consultants_optimized.py\n- consultant_cv.py\n- practices_optimized.py\n- chatbot_service.py\n- document_analyzer.py\n- document_analyzer_clean.py\n- simple_analyzer.py\n\n Objectif : Résoudre ALL les erreurs de syntaxe f-strings pour Python 3.10/Linux\n Pipeline CI/CD maintenant 100% compatible",
          "timestamp": "2025-09-16T15:57:31+02:00",
          "tree_id": "f943cdd85baec08d116cbb903f0313db44ef58cf",
          "url": "https://github.com/ericfunman/Consultator/commit/e94eae001ded5504b26c9af8ae3996bd6836268c"
        },
        "date": 1758031330527,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.2194359204085,
            "unit": "iter/sec",
            "range": "stddev: 0.000001525860181318521",
            "extra": "mean: 1.0624514983821076 msec\nrounds: 927"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 262052.7087754005,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032560312654191255",
            "extra": "mean: 3.816026190582436 usec\nrounds: 87398"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158148.05889370272,
            "unit": "iter/sec",
            "range": "stddev: 8.643893916599645e-7",
            "extra": "mean: 6.323188580342536 usec\nrounds: 75501"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33237.39895282764,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020090590203483893",
            "extra": "mean: 30.086590151631764 usec\nrounds: 25385"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 195.74311116850467,
            "unit": "iter/sec",
            "range": "stddev: 0.000031322416046991525",
            "extra": "mean: 5.108736619288503 msec\nrounds: 197"
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
          "id": "d7f6f317e6253972692c16754b4f847e2c4189da",
          "message": " Correction finale TOUTES f-strings multi-lignes - Fix définitif Linux\n\n Corrections appliquées sur 8 fichiers :\n- chatbot_service.py ligne 865 : Grade consultant\n- simple_analyzer.py ligne 205 : Résultat analyse\n- document_analyzer_clean.py ligne 201 : Éléments extraits\n- document_analyzer.py lignes 365, 562, 1063 : Multiples f-strings\n- consultant_cv.py ligne 761 : Nom fichier rapport\n- practices_optimized.py ligne 274 : Compteur consultants\n- business_managers.py lignes 353, 683 : BM et consultants\n- consultants_clean.py ligne 142 : Info consultant\n\n Objectif : ZÉRO f-string multi-ligne dans le codebase\n Pipeline CI/CD Linux maintenant 100% compatible",
          "timestamp": "2025-09-16T16:07:30+02:00",
          "tree_id": "99442e6a2087154fa842c4ba222019fae5e4977b",
          "url": "https://github.com/ericfunman/Consultator/commit/d7f6f317e6253972692c16754b4f847e2c4189da"
        },
        "date": 1758031917904,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.4205451027956,
            "unit": "iter/sec",
            "range": "stddev: 0.00000502592570784686",
            "extra": "mean: 1.0633540549570744 msec\nrounds: 928"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 275914.21349519474,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010223873794750512",
            "extra": "mean: 3.624314917786632 usec\nrounds: 121419"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158677.93182119378,
            "unit": "iter/sec",
            "range": "stddev: 7.296798018922896e-7",
            "extra": "mean: 6.302073568282009 usec\nrounds: 78716"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32611.549634236115,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018200287319044667",
            "extra": "mean: 30.663982889981543 usec\nrounds: 26768"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.84388173949228,
            "unit": "iter/sec",
            "range": "stddev: 0.000014284212186180777",
            "extra": "mean: 5.080168055837382 msec\nrounds: 197"
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
          "id": "d7f6f317e6253972692c16754b4f847e2c4189da",
          "message": " Correction finale TOUTES f-strings multi-lignes - Fix définitif Linux\n\n Corrections appliquées sur 8 fichiers :\n- chatbot_service.py ligne 865 : Grade consultant\n- simple_analyzer.py ligne 205 : Résultat analyse\n- document_analyzer_clean.py ligne 201 : Éléments extraits\n- document_analyzer.py lignes 365, 562, 1063 : Multiples f-strings\n- consultant_cv.py ligne 761 : Nom fichier rapport\n- practices_optimized.py ligne 274 : Compteur consultants\n- business_managers.py lignes 353, 683 : BM et consultants\n- consultants_clean.py ligne 142 : Info consultant\n\n Objectif : ZÉRO f-string multi-ligne dans le codebase\n Pipeline CI/CD Linux maintenant 100% compatible",
          "timestamp": "2025-09-16T16:07:30+02:00",
          "tree_id": "99442e6a2087154fa842c4ba222019fae5e4977b",
          "url": "https://github.com/ericfunman/Consultator/commit/d7f6f317e6253972692c16754b4f847e2c4189da"
        },
        "date": 1758031933481,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3710247191976,
            "unit": "iter/sec",
            "range": "stddev: 0.000002305845947677968",
            "extra": "mean: 1.0622804120174516 msec\nrounds: 932"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289085.6211004455,
            "unit": "iter/sec",
            "range": "stddev: 6.780222127373907e-7",
            "extra": "mean: 3.459182771503328 usec\nrounds: 107090"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157372.62645421692,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010215456630991338",
            "extra": "mean: 6.354345241171415 usec\nrounds: 80367"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33435.02119724084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016364796662423288",
            "extra": "mean: 29.908759264747317 usec\nrounds: 26336"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.53007810942628,
            "unit": "iter/sec",
            "range": "stddev: 0.000016471143469858147",
            "extra": "mean: 5.0882796649742765 msec\nrounds: 197"
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
          "id": "8d0959c1ab55ee1b63bdc4a18bd8183b8c2ab431",
          "message": " Correction 2 dernières f-strings multi-lignes - Fix FINAL Linux\n\n Corrections critiques :\n- chatbot_service.py ligne 871 : Type de contrat consultant\n- consultant_cv.py ligne 121 : Key bouton compétence\n\n Status : TOUTES les f-strings multi-lignes éliminées du codebase\n Pipeline CI/CD Linux maintenant 100% opérationnel",
          "timestamp": "2025-09-16T16:11:29+02:00",
          "tree_id": "95d433ac7ad23e3a2e4f35050d03e6ad67abafff",
          "url": "https://github.com/ericfunman/Consultator/commit/8d0959c1ab55ee1b63bdc4a18bd8183b8c2ab431"
        },
        "date": 1758032152804,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.2301753632187,
            "unit": "iter/sec",
            "range": "stddev: 0.000006062688007651247",
            "extra": "mean: 1.0635693537634994 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 284428.7889637236,
            "unit": "iter/sec",
            "range": "stddev: 5.86256745096215e-7",
            "extra": "mean: 3.5158185064295346 usec\nrounds: 99414"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156164.34956401173,
            "unit": "iter/sec",
            "range": "stddev: 7.98055370963822e-7",
            "extra": "mean: 6.403510166000469 usec\nrounds: 79284"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33181.604397677926,
            "unit": "iter/sec",
            "range": "stddev: 0.000001880166284241705",
            "extra": "mean: 30.13718046948871 usec\nrounds: 26963"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.51175416654468,
            "unit": "iter/sec",
            "range": "stddev: 0.000014160826286682522",
            "extra": "mean: 5.088754126903244 msec\nrounds: 197"
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
          "id": "8d0959c1ab55ee1b63bdc4a18bd8183b8c2ab431",
          "message": " Correction 2 dernières f-strings multi-lignes - Fix FINAL Linux\n\n Corrections critiques :\n- chatbot_service.py ligne 871 : Type de contrat consultant\n- consultant_cv.py ligne 121 : Key bouton compétence\n\n Status : TOUTES les f-strings multi-lignes éliminées du codebase\n Pipeline CI/CD Linux maintenant 100% opérationnel",
          "timestamp": "2025-09-16T16:11:29+02:00",
          "tree_id": "95d433ac7ad23e3a2e4f35050d03e6ad67abafff",
          "url": "https://github.com/ericfunman/Consultator/commit/8d0959c1ab55ee1b63bdc4a18bd8183b8c2ab431"
        },
        "date": 1758032161678,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.6281998652311,
            "unit": "iter/sec",
            "range": "stddev: 0.000001252597969416849",
            "extra": "mean: 1.061990284640077 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289816.95036853664,
            "unit": "iter/sec",
            "range": "stddev: 5.643447044461885e-7",
            "extra": "mean: 3.4504538079238687 usec\nrounds: 115128"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157872.20198281857,
            "unit": "iter/sec",
            "range": "stddev: 8.004988411285269e-7",
            "extra": "mean: 6.334237360601527 usec\nrounds: 79790"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33059.48990484095,
            "unit": "iter/sec",
            "range": "stddev: 0.000002234956761900956",
            "extra": "mean: 30.248500593276503 usec\nrounds: 26970"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.57911846515157,
            "unit": "iter/sec",
            "range": "stddev: 0.00001500413498926151",
            "extra": "mean: 5.087010297979713 msec\nrounds: 198"
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
          "id": "235b60c646796466ce85d770ff2dac1b9222d734",
          "message": "Trigger CI/CD pipeline",
          "timestamp": "2025-09-16T16:21:56+02:00",
          "tree_id": "95d433ac7ad23e3a2e4f35050d03e6ad67abafff",
          "url": "https://github.com/ericfunman/Consultator/commit/235b60c646796466ce85d770ff2dac1b9222d734"
        },
        "date": 1758033034332,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3155361158151,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031790531401967044",
            "extra": "mean: 1.0623430312500066 msec\nrounds: 928"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 285447.5517373172,
            "unit": "iter/sec",
            "range": "stddev: 6.068624140370921e-7",
            "extra": "mean: 3.5032705444965564 usec\nrounds: 116199"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156740.41844725123,
            "unit": "iter/sec",
            "range": "stddev: 8.303108589543085e-7",
            "extra": "mean: 6.379975311451245 usec\nrounds: 75217"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32964.128930348714,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017691364620790456",
            "extra": "mean: 30.336005605151648 usec\nrounds: 25334"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.50982492702983,
            "unit": "iter/sec",
            "range": "stddev: 0.000021758436032551578",
            "extra": "mean: 5.08880408585846 msec\nrounds: 198"
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
          "id": "235b60c646796466ce85d770ff2dac1b9222d734",
          "message": "Trigger CI/CD pipeline",
          "timestamp": "2025-09-16T16:21:56+02:00",
          "tree_id": "95d433ac7ad23e3a2e4f35050d03e6ad67abafff",
          "url": "https://github.com/ericfunman/Consultator/commit/235b60c646796466ce85d770ff2dac1b9222d734"
        },
        "date": 1758033041607,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.9645770530799,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031419185886847393",
            "extra": "mean: 1.0627392618028275 msec\nrounds: 932"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 300447.1899691726,
            "unit": "iter/sec",
            "range": "stddev: 5.255811102479214e-7",
            "extra": "mean: 3.328371951498715 usec\nrounds: 114195"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158585.60186568976,
            "unit": "iter/sec",
            "range": "stddev: 7.461042361127895e-7",
            "extra": "mean: 6.3057426918676125 usec\nrounds: 80561"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33438.32286009665,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016277358968820587",
            "extra": "mean: 29.90580610708027 usec\nrounds: 27804"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.40934720496446,
            "unit": "iter/sec",
            "range": "stddev: 0.00001204875180595166",
            "extra": "mean: 5.091407380711074 msec\nrounds: 197"
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
          "id": "a7cb413a8213d041a703bd2ac5e5320a101e6794",
          "message": " Fix CRITIQUE: Correction 3 f-strings manquées chatbot_service.py - Fix définitif CI/CD",
          "timestamp": "2025-09-16T16:32:38+02:00",
          "tree_id": "5d8301b3d0c59d466f364ccb029f57ad4dd21403",
          "url": "https://github.com/ericfunman/Consultator/commit/a7cb413a8213d041a703bd2ac5e5320a101e6794"
        },
        "date": 1758033426640,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3994947032633,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015557004929912453",
            "extra": "mean: 1.0622482863295015 msec\nrounds: 929"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 292977.4332046936,
            "unit": "iter/sec",
            "range": "stddev: 5.276642398581342e-7",
            "extra": "mean: 3.413232169664526 usec\nrounds: 111285"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158911.9430912464,
            "unit": "iter/sec",
            "range": "stddev: 9.727791989991973e-7",
            "extra": "mean: 6.292793232197817 usec\nrounds: 79790"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 31798.48357679407,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019475709871771333",
            "extra": "mean: 31.448040520076276 usec\nrounds: 27912"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.54151923816167,
            "unit": "iter/sec",
            "range": "stddev: 0.00001452661814811543",
            "extra": "mean: 5.087983464645134 msec\nrounds: 198"
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
          "id": "a7cb413a8213d041a703bd2ac5e5320a101e6794",
          "message": " Fix CRITIQUE: Correction 3 f-strings manquées chatbot_service.py - Fix définitif CI/CD",
          "timestamp": "2025-09-16T16:32:38+02:00",
          "tree_id": "5d8301b3d0c59d466f364ccb029f57ad4dd21403",
          "url": "https://github.com/ericfunman/Consultator/commit/a7cb413a8213d041a703bd2ac5e5320a101e6794"
        },
        "date": 1758033440940,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 939.8652324406618,
            "unit": "iter/sec",
            "range": "stddev: 0.000005645646731529074",
            "extra": "mean: 1.0639823301083062 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 282525.63237592974,
            "unit": "iter/sec",
            "range": "stddev: 6.924594479480983e-7",
            "extra": "mean: 3.539501855425975 usec\nrounds: 98630"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157329.8404278172,
            "unit": "iter/sec",
            "range": "stddev: 7.525009796082683e-7",
            "extra": "mean: 6.35607331248009 usec\nrounds: 80232"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 31404.776390373805,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016946753212515025",
            "extra": "mean: 31.84229008892164 usec\nrounds: 26940"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.56407356392486,
            "unit": "iter/sec",
            "range": "stddev: 0.00001500382943855691",
            "extra": "mean: 5.087399654824455 msec\nrounds: 197"
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
          "id": "4b29f09c44782bd7f3b1e326f7465fe652ba0011",
          "message": "fix: Corriger les erreurs f-string pour compatibilité Python 3.10\n\n- Convertir les f-strings multi-lignes en single-line dans chatbot_service.py\n- Corriger les f-strings dans business_managers.py\n- Résoudre les erreurs de syntaxe bloquant le CI/CD\n- Tests passent maintenant (469/469)",
          "timestamp": "2025-09-16T16:58:42+02:00",
          "tree_id": "bb824d5ad6303d0ae1efa3a724edbb91f6f13292",
          "url": "https://github.com/ericfunman/Consultator/commit/4b29f09c44782bd7f3b1e326f7465fe652ba0011"
        },
        "date": 1758034988353,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.1420413392326,
            "unit": "iter/sec",
            "range": "stddev: 0.000014779654397979165",
            "extra": "mean: 1.0625388688162452 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 285572.3641495873,
            "unit": "iter/sec",
            "range": "stddev: 6.38738245867883e-7",
            "extra": "mean: 3.5017394031734255 usec\nrounds: 113689"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159258.65536257,
            "unit": "iter/sec",
            "range": "stddev: 7.380083448344697e-7",
            "extra": "mean: 6.279093577196097 usec\nrounds: 76664"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33690.29001885891,
            "unit": "iter/sec",
            "range": "stddev: 0.00000247905251662975",
            "extra": "mean: 29.682142820386144 usec\nrounds: 27265"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.83291700068662,
            "unit": "iter/sec",
            "range": "stddev: 0.000015288232537676303",
            "extra": "mean: 5.080451050758506 msec\nrounds: 197"
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
          "id": "4b29f09c44782bd7f3b1e326f7465fe652ba0011",
          "message": "fix: Corriger les erreurs f-string pour compatibilité Python 3.10\n\n- Convertir les f-strings multi-lignes en single-line dans chatbot_service.py\n- Corriger les f-strings dans business_managers.py\n- Résoudre les erreurs de syntaxe bloquant le CI/CD\n- Tests passent maintenant (469/469)",
          "timestamp": "2025-09-16T16:58:42+02:00",
          "tree_id": "bb824d5ad6303d0ae1efa3a724edbb91f6f13292",
          "url": "https://github.com/ericfunman/Consultator/commit/4b29f09c44782bd7f3b1e326f7465fe652ba0011"
        },
        "date": 1758034994458,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.1677933148604,
            "unit": "iter/sec",
            "range": "stddev: 0.000002053919507956637",
            "extra": "mean: 1.0625097959184604 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289981.28354638745,
            "unit": "iter/sec",
            "range": "stddev: 5.519764851893605e-7",
            "extra": "mean: 3.4484984264166583 usec\nrounds: 105175"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157486.97826011706,
            "unit": "iter/sec",
            "range": "stddev: 7.587564239638165e-7",
            "extra": "mean: 6.349731330474363 usec\nrounds: 81215"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33055.054207927664,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017269344359944252",
            "extra": "mean: 30.25255967543287 usec\nrounds: 27482"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.5247244099511,
            "unit": "iter/sec",
            "range": "stddev: 0.000014428838764911021",
            "extra": "mean: 5.088418279188105 msec\nrounds: 197"
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
          "id": "742f100e541ce4e1cd61ba8e01b8da04559aaa3d",
          "message": "fix: Corriger les dernières erreurs f-string et formatage Black\n\n- Correction f-string ligne 1377 dans chatbot_service.py (chaîne non terminée)\n- Correction f-strings lignes 1577-1580 dans chatbot_service.py\n- Formatage Black pour consultant_skills.py (dict comprehension)\n- Formatage Black pour business_managers.py (parenthèses f-string)\n- Tous les tests passent (469/469) et syntaxe compatible Python 3.10",
          "timestamp": "2025-09-16T17:03:37+02:00",
          "tree_id": "0d9521231d998b03160c415462b2f6da5f09087b",
          "url": "https://github.com/ericfunman/Consultator/commit/742f100e541ce4e1cd61ba8e01b8da04559aaa3d"
        },
        "date": 1758035296351,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.6644478513937,
            "unit": "iter/sec",
            "range": "stddev: 0.000001692795018606383",
            "extra": "mean: 1.061949404888027 msec\nrounds: 941"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 294450.28979340673,
            "unit": "iter/sec",
            "range": "stddev: 4.909571906524401e-7",
            "extra": "mean: 3.396158994109409 usec\nrounds: 114325"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 160409.30175767458,
            "unit": "iter/sec",
            "range": "stddev: 7.450790549104791e-7",
            "extra": "mean: 6.234052446102343 usec\nrounds: 76307"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33194.82531256023,
            "unit": "iter/sec",
            "range": "stddev: 0.000003176562242434189",
            "extra": "mean: 30.125177360750286 usec\nrounds: 27819"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.7373609350635,
            "unit": "iter/sec",
            "range": "stddev: 0.000018826076361723354",
            "extra": "mean: 5.082918644669973 msec\nrounds: 197"
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
          "id": "742f100e541ce4e1cd61ba8e01b8da04559aaa3d",
          "message": "fix: Corriger les dernières erreurs f-string et formatage Black\n\n- Correction f-string ligne 1377 dans chatbot_service.py (chaîne non terminée)\n- Correction f-strings lignes 1577-1580 dans chatbot_service.py\n- Formatage Black pour consultant_skills.py (dict comprehension)\n- Formatage Black pour business_managers.py (parenthèses f-string)\n- Tous les tests passent (469/469) et syntaxe compatible Python 3.10",
          "timestamp": "2025-09-16T17:03:37+02:00",
          "tree_id": "0d9521231d998b03160c415462b2f6da5f09087b",
          "url": "https://github.com/ericfunman/Consultator/commit/742f100e541ce4e1cd61ba8e01b8da04559aaa3d"
        },
        "date": 1758035309448,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.392303774221,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020561622066571585",
            "extra": "mean: 1.062256400430309 msec\nrounds: 929"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 291933.26562078646,
            "unit": "iter/sec",
            "range": "stddev: 5.313586861116325e-7",
            "extra": "mean: 3.4254403925963453 usec\nrounds: 106975"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156958.45272889826,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015138133595187944",
            "extra": "mean: 6.371112753814028 usec\nrounds: 104298"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 31630.030274128887,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030040220495603786",
            "extra": "mean: 31.61552459271368 usec\nrounds: 25719"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.41912226577412,
            "unit": "iter/sec",
            "range": "stddev: 0.0000154482168136295",
            "extra": "mean: 5.091154000000585 msec\nrounds: 197"
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
          "id": "d8a15c13e66393c9176d0c4f04d22248c3a1210e",
          "message": "fix: Remplacer MD5 par SHA-256 dans le service de cache\n\n- Correction du hotspot de sécurité SonarQube\n- Remplacement de hashlib.md5() par hashlib.sha256()\n- Algorithme plus sécurisé pour la génération des clés de cache\n- Compatibilité maintenue, tests passent (469/469)",
          "timestamp": "2025-09-16T17:15:53+02:00",
          "tree_id": "e0710a55e6eab5cad650e1f507d5ca0306708772",
          "url": "https://github.com/ericfunman/Consultator/commit/d8a15c13e66393c9176d0c4f04d22248c3a1210e"
        },
        "date": 1758036156571,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3599876682731,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013575241273164476",
            "extra": "mean: 1.0622928668096216 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 285623.9887752318,
            "unit": "iter/sec",
            "range": "stddev: 4.83872570899767e-7",
            "extra": "mean: 3.5011064871968345 usec\nrounds: 108614"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158260.6627470435,
            "unit": "iter/sec",
            "range": "stddev: 6.836055282596936e-7",
            "extra": "mean: 6.318689576059426 usec\nrounds: 74991"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 31928.367946887804,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016570321771605",
            "extra": "mean: 31.32011011848397 usec\nrounds: 26753"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.3584766319123,
            "unit": "iter/sec",
            "range": "stddev: 0.000015452901613077302",
            "extra": "mean: 5.092726411167724 msec\nrounds: 197"
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
          "id": "d8a15c13e66393c9176d0c4f04d22248c3a1210e",
          "message": "fix: Remplacer MD5 par SHA-256 dans le service de cache\n\n- Correction du hotspot de sécurité SonarQube\n- Remplacement de hashlib.md5() par hashlib.sha256()\n- Algorithme plus sécurisé pour la génération des clés de cache\n- Compatibilité maintenue, tests passent (469/469)",
          "timestamp": "2025-09-16T17:15:53+02:00",
          "tree_id": "e0710a55e6eab5cad650e1f507d5ca0306708772",
          "url": "https://github.com/ericfunman/Consultator/commit/d8a15c13e66393c9176d0c4f04d22248c3a1210e"
        },
        "date": 1758036159275,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3566121373912,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015480588447470308",
            "extra": "mean: 1.0622966759955683 msec\nrounds: 929"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 288379.1442920669,
            "unit": "iter/sec",
            "range": "stddev: 5.245576554052455e-7",
            "extra": "mean: 3.467657144398806 usec\nrounds: 111038"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158700.95332379374,
            "unit": "iter/sec",
            "range": "stddev: 7.461697360569349e-7",
            "extra": "mean: 6.301159375896905 usec\nrounds: 79027"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32624.7863871277,
            "unit": "iter/sec",
            "range": "stddev: 0.000001705276100681271",
            "extra": "mean: 30.651541687781158 usec\nrounds: 27634"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.5664400863643,
            "unit": "iter/sec",
            "range": "stddev: 0.000015420887055891748",
            "extra": "mean: 5.087338406091272 msec\nrounds: 197"
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
          "id": "18f9c368647f8c4ae63574aa49f4757fca7094e6",
          "message": "feat: Amélioration significative de la couverture de test\n\n- Résolution des erreurs de syntaxe bloquant l'exécution des tests\n- Ajout de tests complets pour cache_service.py (96% couverture)\n- Ajout de tests pour document_service.py (78% couverture)\n- Ajout de tests pour chatbot_service.py (13% couverture)\n- Amélioration de consultant_service.py (67% couverture)\n- Correction de conflits de noms dans les fichiers de test\n- Couverture globale actuelle: 39% (objectif: 80% pour SonarQube)\n- 555 tests exécutés avec succès, 1 test en échec à corriger\n\nProchaine étape: Améliorer chatbot_service.py et consultants.py",
          "timestamp": "2025-09-16T18:10:07+02:00",
          "tree_id": "e8377a63f6c92ad945d554d30f57b7c064032542",
          "url": "https://github.com/ericfunman/Consultator/commit/18f9c368647f8c4ae63574aa49f4757fca7094e6"
        },
        "date": 1758039334234,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4675254759462,
            "unit": "iter/sec",
            "range": "stddev: 0.000002477654182614327",
            "extra": "mean: 1.0621715278967945 msec\nrounds: 932"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 285803.50617389474,
            "unit": "iter/sec",
            "range": "stddev: 9.005023708627633e-7",
            "extra": "mean: 3.4989073905606967 usec\nrounds: 79981"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159217.69263935517,
            "unit": "iter/sec",
            "range": "stddev: 7.480247027678921e-7",
            "extra": "mean: 6.280709030654685 usec\nrounds: 78101"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33656.26026400883,
            "unit": "iter/sec",
            "range": "stddev: 0.000001867838357216576",
            "extra": "mean: 29.712154355704673 usec\nrounds: 27022"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.50519500637748,
            "unit": "iter/sec",
            "range": "stddev: 0.000014128821205297437",
            "extra": "mean: 5.088923984770711 msec\nrounds: 197"
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
          "id": "18f9c368647f8c4ae63574aa49f4757fca7094e6",
          "message": "feat: Amélioration significative de la couverture de test\n\n- Résolution des erreurs de syntaxe bloquant l'exécution des tests\n- Ajout de tests complets pour cache_service.py (96% couverture)\n- Ajout de tests pour document_service.py (78% couverture)\n- Ajout de tests pour chatbot_service.py (13% couverture)\n- Amélioration de consultant_service.py (67% couverture)\n- Correction de conflits de noms dans les fichiers de test\n- Couverture globale actuelle: 39% (objectif: 80% pour SonarQube)\n- 555 tests exécutés avec succès, 1 test en échec à corriger\n\nProchaine étape: Améliorer chatbot_service.py et consultants.py",
          "timestamp": "2025-09-16T18:10:07+02:00",
          "tree_id": "e8377a63f6c92ad945d554d30f57b7c064032542",
          "url": "https://github.com/ericfunman/Consultator/commit/18f9c368647f8c4ae63574aa49f4757fca7094e6"
        },
        "date": 1758039339505,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.1889350680462,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017808878360808528",
            "extra": "mean: 1.0624859289571884 msec\nrounds: 929"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 289373.6513263663,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024812382235234955",
            "extra": "mean: 3.455739648086215 usec\nrounds: 109087"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156375.6442189202,
            "unit": "iter/sec",
            "range": "stddev: 8.055714833099728e-7",
            "extra": "mean: 6.394857747796303 usec\nrounds: 75844"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32310.21661951294,
            "unit": "iter/sec",
            "range": "stddev: 0.000001826184239841894",
            "extra": "mean: 30.9499627246719 usec\nrounds: 26130"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.1498283871568,
            "unit": "iter/sec",
            "range": "stddev: 0.00002226145865140434",
            "extra": "mean: 5.098143639596866 msec\nrounds: 197"
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
          "id": "8798f92ae190e539e7e56177b030a7513f0609f8",
          "message": "fix: Correction des workflows CI/CD pour la couverture SonarQube\n\n- Correction du workflow SonarCloud pour utiliser pytest.ini et générer les rapports de couverture\n- Ajout d'exclusions des fichiers de test corrompus dans les workflows CI et SonarCloud\n- Assurance que les rapports de couverture sont générés même en cas d'échec partiel des tests\n- Configuration pour éviter les conflits de noms de fichiers de test\n\nRésout le problème de couverture repassée à 0% sur SonarQube",
          "timestamp": "2025-09-17T06:30:52Z",
          "url": "https://github.com/ericfunman/Consultator/commit/8798f92ae190e539e7e56177b030a7513f0609f8"
        },
        "date": 1758090667675,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 942.0645068355074,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022337065337791587",
            "extra": "mean: 1.061498435345053 msec\nrounds: 928"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 277002.81736026396,
            "unit": "iter/sec",
            "range": "stddev: 9.95723532392574e-7",
            "extra": "mean: 3.610071585298792 usec\nrounds: 118963"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156312.6940785373,
            "unit": "iter/sec",
            "range": "stddev: 7.869732566121483e-7",
            "extra": "mean: 6.397433080499291 usec\nrounds: 107435"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32754.386033156286,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019118822752203535",
            "extra": "mean: 30.530262389523337 usec\nrounds: 26232"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.59854518098118,
            "unit": "iter/sec",
            "range": "stddev: 0.000014987310476714675",
            "extra": "mean: 5.086507629440685 msec\nrounds: 197"
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
          "id": "8798f92ae190e539e7e56177b030a7513f0609f8",
          "message": "fix: Correction des workflows CI/CD pour la couverture SonarQube\n\n- Correction du workflow SonarCloud pour utiliser pytest.ini et générer les rapports de couverture\n- Ajout d'exclusions des fichiers de test corrompus dans les workflows CI et SonarCloud\n- Assurance que les rapports de couverture sont générés même en cas d'échec partiel des tests\n- Configuration pour éviter les conflits de noms de fichiers de test\n\nRésout le problème de couverture repassée à 0% sur SonarQube",
          "timestamp": "2025-09-17T08:30:52+02:00",
          "tree_id": "93a366f01b61444074ce0a33bd49ec91f002488e",
          "url": "https://github.com/ericfunman/Consultator/commit/8798f92ae190e539e7e56177b030a7513f0609f8"
        },
        "date": 1758090930801,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.3218770141083,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016204544159735914",
            "extra": "mean: 1.0623358751334029 msec\nrounds: 929"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 285556.9635843068,
            "unit": "iter/sec",
            "range": "stddev: 5.321173439376674e-7",
            "extra": "mean: 3.501928257843951 usec\nrounds: 103649"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157528.4215440973,
            "unit": "iter/sec",
            "range": "stddev: 8.224970191712017e-7",
            "extra": "mean: 6.348060814664277 usec\nrounds: 76133"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32536.881535026587,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021259265274289083",
            "extra": "mean: 30.73435291957776 usec\nrounds: 27332"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.3692449289796,
            "unit": "iter/sec",
            "range": "stddev: 0.00001564458872521406",
            "extra": "mean: 5.092447141412942 msec\nrounds: 198"
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
          "id": "8798f92ae190e539e7e56177b030a7513f0609f8",
          "message": "fix: Correction des workflows CI/CD pour la couverture SonarQube\n\n- Correction du workflow SonarCloud pour utiliser pytest.ini et générer les rapports de couverture\n- Ajout d'exclusions des fichiers de test corrompus dans les workflows CI et SonarCloud\n- Assurance que les rapports de couverture sont générés même en cas d'échec partiel des tests\n- Configuration pour éviter les conflits de noms de fichiers de test\n\nRésout le problème de couverture repassée à 0% sur SonarQube",
          "timestamp": "2025-09-17T08:30:52+02:00",
          "tree_id": "93a366f01b61444074ce0a33bd49ec91f002488e",
          "url": "https://github.com/ericfunman/Consultator/commit/8798f92ae190e539e7e56177b030a7513f0609f8"
        },
        "date": 1758090934452,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.2322960961311,
            "unit": "iter/sec",
            "range": "stddev: 0.00002293182848288445",
            "extra": "mean: 1.0635669548387414 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 288433.7467365121,
            "unit": "iter/sec",
            "range": "stddev: 8.373992246107963e-7",
            "extra": "mean: 3.4670006936238043 usec\nrounds: 61997"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 159459.83879906812,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012575510800213849",
            "extra": "mean: 6.271171522129018 usec\nrounds: 80561"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 32997.23992111888,
            "unit": "iter/sec",
            "range": "stddev: 0.000003939452270531935",
            "extra": "mean: 30.30556502272726 usec\nrounds: 18109"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.7325704813866,
            "unit": "iter/sec",
            "range": "stddev: 0.00001709616814617938",
            "extra": "mean: 5.0830424141416515 msec\nrounds: 198"
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
          "id": "8798f92ae190e539e7e56177b030a7513f0609f8",
          "message": "fix: Correction des workflows CI/CD pour la couverture SonarQube\n\n- Correction du workflow SonarCloud pour utiliser pytest.ini et générer les rapports de couverture\n- Ajout d'exclusions des fichiers de test corrompus dans les workflows CI et SonarCloud\n- Assurance que les rapports de couverture sont générés même en cas d'échec partiel des tests\n- Configuration pour éviter les conflits de noms de fichiers de test\n\nRésout le problème de couverture repassée à 0% sur SonarQube",
          "timestamp": "2025-09-17T06:30:52Z",
          "url": "https://github.com/ericfunman/Consultator/commit/8798f92ae190e539e7e56177b030a7513f0609f8"
        },
        "date": 1758091230306,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.4213989168002,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021230489665603616",
            "extra": "mean: 1.0622235708160026 msec\nrounds: 932"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 293760.94102937315,
            "unit": "iter/sec",
            "range": "stddev: 4.929693395871105e-7",
            "extra": "mean: 3.4041285287822185 usec\nrounds: 120121"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 157924.76562432252,
            "unit": "iter/sec",
            "range": "stddev: 7.010498473596224e-7",
            "extra": "mean: 6.332129074541977 usec\nrounds: 77676"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33394.43777425979,
            "unit": "iter/sec",
            "range": "stddev: 0.000002229331133149488",
            "extra": "mean: 29.945106630026668 usec\nrounds: 27497"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.6767619384735,
            "unit": "iter/sec",
            "range": "stddev: 0.000016306978047162156",
            "extra": "mean: 5.084484766496362 msec\nrounds: 197"
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
          "id": "235278c1fbc30af7232bc80dd15cc6664f0fb110",
          "message": "fix: Résoudre les conflits de fichiers de test et corriger le workflow CI/CD\n\n- Supprimer le fichier test_simple.py conflictuel à la racine\n- Corriger le test test_update_consultant_info_salary_change_with_history\n- Mettre à jour le workflow SonarCloud pour initialiser la DB et générer le rapport de couverture\n- Résultat: Couverture de test maintenant correctement rapportée à SonarQube (39% au lieu de 0%)",
          "timestamp": "2025-09-17T08:54:55+02:00",
          "tree_id": "e700f8834ab5b9e1bcd4092d3db5dcd6e95551e6",
          "url": "https://github.com/ericfunman/Consultator/commit/235278c1fbc30af7232bc80dd15cc6664f0fb110"
        },
        "date": 1758092372462,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.5050363937805,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011106101871089073",
            "extra": "mean: 1.0621292094519972 msec\nrounds: 931"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 296069.9040045353,
            "unit": "iter/sec",
            "range": "stddev: 5.177788890741562e-7",
            "extra": "mean: 3.3775807215605465 usec\nrounds: 114864"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156440.18711074695,
            "unit": "iter/sec",
            "range": "stddev: 7.351092514645826e-7",
            "extra": "mean: 6.392219406462876 usec\nrounds: 77737"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33761.20697705784,
            "unit": "iter/sec",
            "range": "stddev: 0.000002668774646232039",
            "extra": "mean: 29.61979412286836 usec\nrounds: 27905"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.6540640660027,
            "unit": "iter/sec",
            "range": "stddev: 0.00001522085199298738",
            "extra": "mean: 5.085071619289655 msec\nrounds: 197"
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
          "id": "235278c1fbc30af7232bc80dd15cc6664f0fb110",
          "message": "fix: Résoudre les conflits de fichiers de test et corriger le workflow CI/CD\n\n- Supprimer le fichier test_simple.py conflictuel à la racine\n- Corriger le test test_update_consultant_info_salary_change_with_history\n- Mettre à jour le workflow SonarCloud pour initialiser la DB et générer le rapport de couverture\n- Résultat: Couverture de test maintenant correctement rapportée à SonarQube (39% au lieu de 0%)",
          "timestamp": "2025-09-17T08:54:55+02:00",
          "tree_id": "e700f8834ab5b9e1bcd4092d3db5dcd6e95551e6",
          "url": "https://github.com/ericfunman/Consultator/commit/235278c1fbc30af7232bc80dd15cc6664f0fb110"
        },
        "date": 1758092386474,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 940.5307284844316,
            "unit": "iter/sec",
            "range": "stddev: 0.000005416222613423561",
            "extra": "mean: 1.063229482795737 msec\nrounds: 930"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 291370.4825362358,
            "unit": "iter/sec",
            "range": "stddev: 5.521107738857343e-7",
            "extra": "mean: 3.4320566424419345 usec\nrounds: 122011"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 158587.88200853206,
            "unit": "iter/sec",
            "range": "stddev: 7.039268235999768e-7",
            "extra": "mean: 6.305652029240164 usec\nrounds: 79340"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33254.51714382572,
            "unit": "iter/sec",
            "range": "stddev: 0.000003160376704705499",
            "extra": "mean: 30.071102691853927 usec\nrounds: 27490"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.54371609787518,
            "unit": "iter/sec",
            "range": "stddev: 0.000015102245334500786",
            "extra": "mean: 5.087926593908596 msec\nrounds: 197"
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
          "id": "9dfdcdaf6c411d6e9d6fa43925178bacc5f3da2b",
          "message": "feat: Amélioration significative de la couverture de tests pour conformité SonarQube\n\n- Expansion majeure des tests unitaires pour ChatbotService (36+ tests)\n- Création complète de tests pour DocumentAnalyzer (15 tests)\n- Tests exhaustifs pour SimpleDocumentAnalyzer (extraction fichiers)\n- Tests complets pour TechnologyService avec gestion d'erreurs\n- Tests UI pour TechnologyWidget avec mocking Streamlit\n- Correction des erreurs SQLAlchemy dans les tests\n- Amélioration du mocking pour les interactions DB et UI\n- Couverture de tests dépassant 80% pour tous les services critiques\n- Préparation pour analyse SonarQube et validation qualité code",
          "timestamp": "2025-09-17T09:53:44+02:00",
          "tree_id": "a3ae445a1896ce216b80bf351c6323ec6146b1bc",
          "url": "https://github.com/ericfunman/Consultator/commit/9dfdcdaf6c411d6e9d6fa43925178bacc5f3da2b"
        },
        "date": 1758096275037,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_database_connection_speed",
            "value": 941.153355059152,
            "unit": "iter/sec",
            "range": "stddev: 0.000001871216341639926",
            "extra": "mean: 1.062526095906176 msec\nrounds: 928"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_data_processing_speed",
            "value": 291725.4076080782,
            "unit": "iter/sec",
            "range": "stddev: 5.822549342244813e-7",
            "extra": "mean: 3.4278810618493036 usec\nrounds: 112033"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_ui_rendering_simulation",
            "value": 156620.5389287797,
            "unit": "iter/sec",
            "range": "stddev: 7.907046342062078e-7",
            "extra": "mean: 6.384858632460277 usec\nrounds: 72591"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_memory_usage_simulation",
            "value": 33347.46527891053,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022800880001317277",
            "extra": "mean: 29.98728663891633 usec\nrounds: 27512"
          },
          {
            "name": "tests/test_performance_v14.py::TestPerformance::test_api_response_simulation",
            "value": 196.5304490579347,
            "unit": "iter/sec",
            "range": "stddev: 0.000014520327609471762",
            "extra": "mean: 5.08827006091668 msec\nrounds: 197"
          }
        ]
      }
    ]
  }
}