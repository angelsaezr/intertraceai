import 'package:go_router/go_router.dart';
import 'package:intertraceai/features/doc/presentation/screens/docs_screen.dart';
import 'package:intertraceai/shared/layout/app_layout.dart';
import 'package:intertraceai/features/chat/presentation/screens/chat_screen.dart';
import 'package:intertraceai/features/info/presentation/screens/info_screen.dart';

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
          path: '/docs',
          builder: (context, state) => const DocsScreen(),
        ),
        GoRoute(
          path: '/info',
          builder: (context, state) => const InfoScreen(),
        ),
      ],
    ),
  ],
);
