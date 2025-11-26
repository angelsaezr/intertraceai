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
    state = [...state, ChatMessage(text: text, isUser: true)];

    try {
      final reply = await _repository.sendQuery(text);

      state = [...state, ChatMessage(text: reply, isUser: false)];
    } catch (e) {
      state = [...state, ChatMessage(text: "Error: $e", isUser: false)];
    }
  }
}

final chatProvider = NotifierProvider<ChatController, List<ChatMessage>>(
  ChatController.new,
);
