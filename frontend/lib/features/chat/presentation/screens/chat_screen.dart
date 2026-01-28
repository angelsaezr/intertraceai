import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intertraceai/core/theme/app_colors.dart';
import '../../controller/chat_controller.dart';
import '../widgets/message_bubble.dart';

class ChatScreen extends ConsumerStatefulWidget {
  const ChatScreen({super.key});

  @override
  ConsumerState<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends ConsumerState<ChatScreen> {
  final TextEditingController _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final messages = ref.watch(chatProvider);

    return Column(
      children: [
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.only(bottom: 16),
            itemCount: messages.length,
            itemBuilder: (context, index) {
              final msg = messages[index];
              return MessageBubble(
                text: msg.text,
                isUser: msg.isUser,
                isLoading: msg.isLoading,
              );
            },
          ),
        ),

        Row(
          children: [
            Expanded(
              child: TextField(
                controller: _controller,
                textInputAction: TextInputAction.send,
                onSubmitted: (value) {
                  if (value.trim().isNotEmpty) {
                    ref.read(chatProvider.notifier).sendMessage(value.trim());
                    _controller.clear();
                  }
                },
                decoration: const InputDecoration(
                  hintText: "Ask something...",
                  enabledBorder: UnderlineInputBorder(
                    borderSide: BorderSide(color: AppColors.primary),
                  ),
                  focusedBorder: UnderlineInputBorder(
                    borderSide: BorderSide(color: AppColors.primary, width: 2),
                  ),
                ),
                cursorColor: AppColors.primary,
              ),
            ),
            const SizedBox(width: 10),
            IconButton(
              icon: const Icon(Icons.send),
              color: AppColors.primary,
              tooltip: "Send",
              onPressed: () {
                if (_controller.text.trim().isNotEmpty) {
                  ref
                      .read(chatProvider.notifier)
                      .sendMessage(_controller.text.trim());
                  _controller.clear();
                }
              },
            ),
          ],
        ),
      ],
    );
  }
}
