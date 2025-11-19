import 'package:go_router/go_router.dart';
import '../../shared/layout/app_layout.dart';
import '../../features/chat/presentation/screens/chat_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/chat',

  routes: [
    ShellRoute(
      builder: (context, state, child) => AppLayout(child: child),
      routes: [
        GoRoute(
          path: '/chat',
          builder: (context, state) => const ChatScreen(),
        ),
      ],
    ),
  ],
);
