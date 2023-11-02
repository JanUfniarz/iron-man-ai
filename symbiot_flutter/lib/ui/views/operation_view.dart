import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../control/controllers/operation_controller.dart';
import '../palette.dart';
import '../widgets/input_bar.dart';
import '../widgets/symbiot_divider.dart';
import '../widgets/symbiot_scaffold.dart';

class OperationView extends StatelessWidget {

  final String id;

  const OperationView(this.id, {super.key});

  @override
  Widget build(BuildContext context) => Consumer<OperationController>(
        builder: (context, controller, child) => SymbiotScaffold(
          tittle: controller.operation(id).name,
          body: Column(
            children: [
              InputBar(
                onSend: (text) {}, // TODO: new step
                child: Align(
                  alignment: Alignment.topCenter,
                  child: SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: <Widget>[
                        Padding(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          child: Text(
                            "The main purpose of this operation is:\n"
                            "${controller.operation(id).nordStar}",
                            style: const TextStyle(
                              color: Palette.accent,
                              fontSize: 25,
                            ),
                          ),
                        ),
                        const SymbiotDivider(),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: List.generate(
                              controller.operation(id).records.length,
                              (index) => InkWell(
                                    onTap: () => controller.openChat(
                                        controller.operation(id)
                                            .records[index],
                                        context
                                    ),
                                    child: Card(
                                      child: Padding(
                                        padding: const EdgeInsets.all(20),
                                        child: Text(controller
                                            .operation(id).records[index].id
                                            .toString()),
                                      ),
                                    ),
                              )
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      );
}