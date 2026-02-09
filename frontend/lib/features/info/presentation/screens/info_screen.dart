import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intertraceai/core/theme/app_colors.dart';
import '../../controller/ingest_controller.dart';

class InfoScreen extends ConsumerWidget {
  const InfoScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final ui = ref.watch(ingestProvider);

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "Info",
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),

          ElevatedButton.icon(
            icon: ui.loading
                ? const SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.refresh),
            label: Text(ui.loading ? "Ingesting..." : "Ingest"),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primary,
              foregroundColor: Colors.white,
            ),
            onPressed: ui.loading
                ? null
                : () => ref.read(ingestProvider.notifier).resetAndIngest(),
          ),

          const SizedBox(height: 16),

          if (ui.result != null)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.layoutBackground,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(ui.result!),
            ),
        ],
      ),
    );
  }
}
