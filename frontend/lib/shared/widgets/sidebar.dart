import 'package:flutter/material.dart';
import 'package:intertraceai/core/theme/app_colors.dart';
import 'sidebar_item.dart';

class Sidebar extends StatelessWidget {
  final bool collapsed;

  const Sidebar({super.key, required this.collapsed});

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      width: collapsed ? 72 : 140,
      color: AppColors.layoutBackground,
      child: Column(
        children: [
          SidebarItem(
            icon: Icons.chat_bubble,
            label: "Chat",
            route: "/chat",
            collapsed: collapsed,
          ),

          SidebarItem(
            icon: Icons.description,
            label: "Docs",
            route: "/docs",
            collapsed: collapsed,
          ),

          Spacer(),

          SidebarItem(
            icon: Icons.info,
            label: "Info",
            route: "/info",
            collapsed: collapsed,
          ),
        ],
      ),
    );
  }
}
