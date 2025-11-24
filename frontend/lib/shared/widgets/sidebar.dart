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
            icon: Icons.add,
            label: "New chat",
            route: "/chat",
            collapsed: collapsed,
          ),

          SidebarItem(
            icon: Icons.history,
            label: "History",
            route: "/history",
            collapsed: collapsed,
          ),

          Spacer(),

          SidebarItem(
            icon: Icons.settings,
            label: "Settings",
            route: "/settings",
            collapsed: collapsed,
          ),
        ],
      ),
    );
  }
}
