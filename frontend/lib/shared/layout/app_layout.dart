import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intertraceai/shared/providers/sidebar_state.dart';
import 'package:intertraceai/core/theme/app_colors.dart';
import 'package:intertraceai/shared/widgets/sidebar.dart';

class AppLayout extends ConsumerWidget {
  final Widget child;

  const AppLayout({super.key, required this.child});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final collapsed = ref.watch(sidebarCollapsedProvider);

    return Scaffold(
      backgroundColor: AppColors.appBackground,

      appBar: AppBar(
        backgroundColor: AppColors.layoutBackground,

        leading: Align(
          alignment: Alignment.centerRight,
          child: IconButton(
            icon: Icon(collapsed ? Icons.menu : Icons.close),
            onPressed: () =>
              ref.read(sidebarCollapsedProvider.notifier).toggle(),
          ),
        ),

        title: Row(
          children: [
            const SizedBox(width: 10),
            Image.asset(
              "assets/images/icon.png",
              height: 32,
              width: 32,
            ),
            const SizedBox(width: 10),
            const Text("InterTraceAI"),
          ],
        ),
      ),

      body: Row(
        children: [
          Sidebar(collapsed: collapsed),

          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: child,
            ),
          ),
        ],
      ),
    );
  }
}
