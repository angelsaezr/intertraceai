import 'package:flutter_riverpod/flutter_riverpod.dart';

class SidebarStateNotifier extends Notifier<bool> {
  @override
  bool build() => false;

  void toggle() => state = !state;
}

final sidebarCollapsedProvider =
    NotifierProvider<SidebarStateNotifier, bool>(SidebarStateNotifier.new);
