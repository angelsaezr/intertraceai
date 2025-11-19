import 'package:flutter/material.dart';
import 'sidebar_item.dart';

class Sidebar extends StatelessWidget {
  final bool collapsed;

  const Sidebar({super.key, required this.collapsed});

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      width: collapsed ? 68 : 150,
      color: Colors.grey.shade900,
      child: Column(
        children: [

          SidebarItem(
            icon: Icons.chat,
            label: "Chat",
            route: "/chat",
            collapsed: collapsed,
          ),
        ],
      ),
    );
  }
}
