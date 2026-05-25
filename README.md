# patrolbot_navigation2

`patrolbot_navigation2` is a ROS 2 Jazzy package scaffold for PatrolBot navigation workflows. 

## Repository Structure

- `config/` stores YAML parameter files for navigation, SLAM, multiplexing, and robot-specific tuning.
- `launch/` contains ROS 2 launch descriptions that assemble the navigation stack from composable, reusable components.
- `maps/` holds occupancy grid maps, SLAM outputs, and map metadata used for localization and route planning.
- `scripts/` is reserved for executable Python utilities, operator helpers, and small integration tools.
- `src/` is available for package-local source code when reusable logic should live outside launch or configuration files.
- `package.xml` declares package identity, build type, and ROS 2 dependencies.


## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for the full text.