import 'package:flutter/material.dart';
import 'package:intertraceai/core/theme/app_colors.dart';

class MessageBubble extends StatelessWidget {
  final String text;
  final bool isUser;
  final bool isLoading;

  const MessageBubble({
    super.key,
    required this.text,
    required this.isUser,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 6),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isUser ? AppColors.primary : AppColors.layoutBackground,
          borderRadius: BorderRadius.circular(12),
        ),
        child: isLoading
            ? const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(strokeWidth: 2, color: AppColors.primary),
              )
            : Text(text),
      ),
    );
  }
}
