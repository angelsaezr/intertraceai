import 'package:flutter/material.dart';
import 'package:intertraceai/core/theme/app_colors.dart';
import 'package:intertraceai/shared/widgets/sidebar.dart';

class AppLayout extends StatefulWidget {
  final Widget child;

  const AppLayout({super.key, required this.child});

  @override
  State<AppLayout> createState() => _AppLayoutState();
}

class _AppLayoutState extends State<AppLayout> {
  bool collapsed = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.appBackground,
      appBar: AppBar(
        backgroundColor: AppColors.layoutBackground,
        leading: IconButton(
          icon: Icon(collapsed ? Icons.menu : Icons.close),
          onPressed: () => setState(() => collapsed = !collapsed),
        ),

        title: Row(
          children: [
            SizedBox(width: 10),
            Image.asset(
              "assets/images/icon.png",
              height: 32,
              width: 32,
            ),
            SizedBox(width: 10),
            Text("InterTraceAI"),
          ],
        ),
      ),

      body: Row(
        children: [
          Sidebar(collapsed: collapsed),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: widget.child,
            ),
          ),
        ],
      ),
    );
  }
}
