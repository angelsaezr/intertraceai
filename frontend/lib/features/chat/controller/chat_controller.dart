import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intertraceai/features/chat/model/chat_message.dart';
import 'package:intertraceai/features/chat/repository/chat_repository.dart';

class ChatController extends Notifier<List<ChatMessage>> {
  late final ChatRepository _repository;

  @override
  List<ChatMessage> build() {
    _repository = ChatRepository(baseUrl: "http://127.0.0.1:8000");
    return [];
  }

  Future<void> sendMessage(String text) async {
    // User message
    state = [
      ...state,
      ChatMessage(text: text, isUser: true),
      ChatMessage(text: "", isUser: false, isLoading: true), // loading
    ];

    try {
      final reply = await _repository.sendQuery(text);

      // Remove loading and add reply
      state = [
        ...state.where((m) => !m.isLoading),
        ChatMessage(text: reply, isUser: false),
      ];
    } catch (e) {
      state = [
        ...state.where((m) => !m.isLoading),
        ChatMessage(text: "Error: $e", isUser: false),
      ];
    }
  }
}

final chatProvider = NotifierProvider<ChatController, List<ChatMessage>>(
  ChatController.new,
);
