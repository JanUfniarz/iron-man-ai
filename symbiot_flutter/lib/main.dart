import 'package:flutter/material.dart';

import 'connection/operation_connector.dart';
import 'tests/api_control_panel.dart';

// void main() {
//
//   runApp(MaterialApp(
//     home: HomeView(
//       connector: FirstConnector(),
//     ),
//   ));
// }

void main() => runApp(MaterialApp(
  home: ApiControlPanel(
    connector: OperationConnector(),
  ),
));