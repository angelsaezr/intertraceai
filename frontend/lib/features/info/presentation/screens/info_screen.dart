import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intertraceai/core/theme/app_colors.dart';
import '../../controller/ingest_controller.dart';

class InfoScreen extends ConsumerWidget {
  const InfoScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final ui = ref.watch(ingestProvider);
    final documentsFolder = '${Platform.environment['HOME'] ?? Platform.environment['USERPROFILE']}/Documents';

    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.settings, size: 26),
              SizedBox(width: 10),
              Text(
                "System configuration",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
            ],
          ),

          const SizedBox(height: 24),

          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: AppColors.layoutBackground,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  "Search engine parameters",
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 16),
                _configRow("Documents folder", documentsFolder),
                _configRow("Max depth", "3"),
                _configRow("Max directory size (MB)", "200"),
                _configRow("Allowed extensions", ".pdf"),
                _configRow("Max documents", "10"),
                _configRow("Max PDF size (MB)", "10"),
              ],
            ),
          ),

          const SizedBox(height: 20),

          if (ui.result != null)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.layoutBackground,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(ui.result!, style: const TextStyle(fontSize: 14)),
            ),

          const Spacer(),

          Center(
            child: SizedBox(
              width: 240,
              child: ElevatedButton.icon(
                icon: ui.loading
                    ? const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          valueColor:
                              AlwaysStoppedAnimation<Color>(AppColors.primary),
                        ),
                      )
                    : const Icon(Icons.sync),
                label: Text(
                  ui.loading ? "Ingesting..." : "Ingest",
                  style: const TextStyle(fontSize: 15),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(14),
                  ),
                ),
                onPressed: ui.loading
                    ? null
                    : () => ref.read(ingestProvider.notifier).resetAndIngest(),
              ),
            ),
          ),
        ],
      ),
    );
  }

  static Widget _configRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        children: [
          Expanded(child: Text(label, style: const TextStyle(fontSize: 14))),
          Flexible(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              decoration: BoxDecoration(
                color: Colors.black.withValues(alpha: 0.04),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                value,
                style: const TextStyle(
                  fontFamily: 'monospace',
                  fontWeight: FontWeight.w600,
                ),
                overflow: TextOverflow.ellipsis,
                maxLines: 2,
              ),
            ),
          ),
        ],
      ),
    );
  }
}