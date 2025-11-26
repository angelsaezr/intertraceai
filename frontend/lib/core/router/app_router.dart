import 'package:go_router/go_router.dart';
import 'package:intertraceai/features/history/presentation/screens/history_screen.dart';
import 'package:intertraceai/shared/layout/app_layout.dart';
import 'package:intertraceai/features/chat/presentation/screens/chat_screen.dart';
import 'package:intertraceai/features/settings/presentation/screens/settings_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/',

  routes: [
    ShellRoute(
      builder: (context, state, child) => AppLayout(child: child),
      routes: [
        GoRoute(
          path: '/',
          builder: (context, state) => const ChatScreen(),
        ),
        GoRoute(
          path: '/chat',
          builder: (context, state) => const ChatScreen(),
        ),
        GoRoute(
          path: '/history',
          builder: (context, state) => const HistoryScreen(),
        ),
        GoRoute(
          path: '/settings',
          builder: (context, state) => const SettingsScreen(),
        ),
      ],
    ),
  ],
);
