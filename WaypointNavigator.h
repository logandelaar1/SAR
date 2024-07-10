#ifndef WAYPOINTNAVIGATOR_H
#define WAYPOINTNAVIGATOR_H

#include "MOOS/libMOOS/App/MOOSApp.h"
#include <vector>
#include <string>
#include <utility>

class WaypointNavigator : public CMOOSApp {
public:
    bool OnStartUp();
    bool Iterate();
    bool OnNewMail(MOOSMSG_LIST &NewMail);

private:
    void MoveTowards(double target_lat, double target_lon);
    bool WithinDistance(double lat1, double lon1, double lat2, double lon2, double distance_threshold);
    void UpdateDynamicLocation();

    std::vector<std::pair<double, double>> waypoints;
    size_t current_waypoint_index;
    double dynamic_lat, dynamic_lon;
    bool dynamic_location_active;
    double current_lat, current_lon; // Current position of the boat
};

#endif // WAYPOINTNAVIGATOR_H