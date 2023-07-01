# Android Monitoring System

The Android Monitoring System is a monitoring solution that captures and analyzes logcat logs from Android devices. It provides real-time log monitoring, log storage, and analysis capabilities to help track and diagnose issues in Android applications.

## Purpose per Version

### v1 : Make monitoring system for process info in android device
### v2 : Make monitoring system using android logcat

----

## Feature in Progress

This section provides an overview of the key features currently under development in the Android Monitoring System:


### Feature 1: Stack log data in DataLake from user phone
Description: Implement real-time log stack system from user phone.

#### Progress:

> Completed 
- log collection from Android devices using ADB.
- streams data to Logstash using Filebeat

> In progress 
- Get Process info from Android Phone


----

## Planned Feature

This section outlines the features that are currently in the planning phase for the Android Monitoring System:

### Feature : Real-time Log Analysis
Description: Implement real-time log analysis capabilities to perform advanced parsing, filtering, and analysis of log data from connected Android devices.

- Objective 1: Develop a flexible log parsing mechanism to extract structured data from log messages.
- Objective 2: Implement advanced filtering options to allow users to narrow down log results based on specific criteria.
- Objective 3: Enable real-time log analysis and visualization through interactive charts and graphs.

### Feature 3: Performance Monitoring
Description: Add performance monitoring capabilities to track the performance of Android applications based on log data.

- Objective 1: Monitor resource usage (CPU, memory, network) from log metrics.
- Objective 2: Generate performance metrics and visualizations to identify bottlenecks and optimize application performance.
- Objective 3: Integrate with existing performance monitoring tools or frameworks (e.g., Grafana) for a comprehensive view.
