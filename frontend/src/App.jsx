
import { useState, useEffect } from "react";
import { getSystemHealth } from "./services/api";
import Assistant from "./Assistant";

import {
  Shield, LayoutDashboard, Camera, Bell, Bot,
  Activity, Settings, FileText, Search,
  Menu, ShieldAlert, Users, Wifi,
  ChevronRight, ArrowUpRight, Radio,
  CircleAlert, CheckCircle2, Clock,
  ScanEye
} from "lucide-react";

import {
  ResponsiveContainer, AreaChart, Area,
  XAxis, YAxis, Tooltip, CartesianGrid
} from "recharts";

import "./App.css";

const navigation = [
  { name: "Overview", icon: LayoutDashboard },
  { name: "Live Monitoring", icon: Camera },
  { name: "Incidents", icon: ShieldAlert },
  { name: "Analytics", icon: Activity },
  { name: "Cameras", icon: Radio },
  { name: "Reports", icon: FileText },
  { name: "AI Assistant", icon: Bot },
  { name: "Settings", icon: Settings },
];

const chartData = [
  { time: "08:00", incidents: 3 },
  { time: "09:00", incidents: 5 },
  { time: "10:00", incidents: 2 },
  { time: "11:00", incidents: 8 },
  { time: "12:00", incidents: 4 },
  { time: "13:00", incidents: 6 },
  { time: "14:00", incidents: 3 },
];

const incidents = [
  {
    id: "INC-001",
    type: "Missing Safety Helmet",
    camera: "CAM-01",
    time: "10:42:18",
    severity: "High",
    status: "Unresolved",
  },
  {
    id: "INC-002",
    type: "Restricted Zone Entry",
    camera: "CAM-03",
    time: "10:38:42",
    severity: "Critical",
    status: "Unresolved",
  },
  {
    id: "INC-003",
    type: "Missing Safety Vest",
    camera: "CAM-02",
    time: "10:25:09",
    severity: "Medium",
    status: "Resolved",
  },
];

function App() {
  const [systemHealth, setSystemHealth] = useState(null);
  const [active, setActive] = useState("Overview");
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    const fetchHealth = async () => {
      const data = await getSystemHealth();

      if (data) {
        setSystemHealth(data);
      }
    };

    fetchHealth();

    const interval = setInterval(fetchHealth, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">

      {/* SIDEBAR */}

      <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>

        <div className="brand">
          <div className="brand-icon">
            <Shield size={25} />
          </div>

          {!collapsed && (
            <div>
              <h2>SENTINEL<span>AI</span></h2>
              <p>INTELLIGENT SURVEILLANCE</p>
            </div>
          )}
        </div>

        <div className="nav-label">
          {!collapsed && "WORKSPACE"}
        </div>

        <nav>
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`nav-item ${
                  active === item.name ? "active" : ""
                }`}
                onClick={() => setActive(item.name)}
                title={item.name}
              >
                <Icon size={19} />

                {!collapsed && <span>{item.name}</span>}

                {item.name === "Incidents" && !collapsed && (
                  <span className="nav-count">3</span>
                )}
              </button>
            );
          })}
        </nav>

        <div className="sidebar-bottom">

          <div className="system-status">
            <span className="status-dot"></span>

            {!collapsed && (
              <div>
                <strong>System Online</strong>
                <small>All services operational</small>
              </div>
            )}
          </div>

          {!collapsed && (
            <div className="version">
              SENTINEL AI v1.0.0
            </div>
          )}

        </div>

      </aside>

      {/* MAIN CONTENT */}

      <main className="main">

        {/* HEADER */}

        <header className="topbar">

          <div className="header-left">

            <button
              className="icon-button"
              onClick={() => setCollapsed(!collapsed)}
            >
              <Menu size={20} />
            </button>

            <div>
              <div className="breadcrumb">
                WORKSPACE <ChevronRight size={12} /> {active.toUpperCase()}
              </div>

              <h1>{active}</h1>
            </div>

          </div>

          <div className="header-right">

            <div className="live-indicator">
              <span></span> SYSTEM ACTIVE
            </div>

            <button className="icon-button notification">
              <Bell size={19} />
              <i></i>
            </button>

            <div className="profile">
              <div className="avatar">SA</div>

              <div>
                <strong>Administrator</strong>
                <small>System Admin</small>
              </div>
            </div>

          </div>

        </header>

        {/* PAGE CONTENT */}

        {active === "AI Assistant" ? (

          <Assistant />

        ) : (

          <div className="content">

            {/* WELCOME */}

            <div className="welcome">

              <div>
                <p className="eyebrow">
                  INTELLIGENT SAFETY MONITORING SYSTEM
                </p>

                <h2>Security Overview<span>.</span></h2>

                <p className="welcome-text">
                  Monitor your environment. Detect threats.
                  Prevent incidents.
                </p>
              </div>

              <div className="date-box">
                <Clock size={16} />
                REAL-TIME MONITORING
              </div>

            </div>

            {/* STATISTICS */}

            <section className="stats-grid">

              <StatCard
                icon={Camera}
                label="Total Cameras"
                value="04"
                detail="2 currently active"
                color="blue"
              />

              <StatCard
                icon={ShieldAlert}
                label="Total Incidents"
                value="12"
                detail="3 require attention"
                color="red"
              />

              <StatCard
                icon={Activity}
                label="Safety Compliance"
                value="87.4%"
                detail="Demo metric"
                color="green"
              />

              <StatCard
                icon={Users}
                label="Objects Detected"
                value="148"
                detail="Demo detection count"
                color="purple"
              />

            </section>

            {/* MONITORING + ALERTS */}

            <section className="dashboard-grid">

              <div className="panel monitoring-panel">

                <div className="panel-header">

                  <div>
                    <h3>Live Monitoring</h3>
                    <p>Camera surveillance overview</p>
                  </div>

                  <span className="recording">
                    <span></span> DEMO
                  </span>

                </div>

                <div className="camera-screen">

                  <div className="camera-top">
                    <span>CAM-01 / MAIN ENTRANCE</span>
                    <span>DEMO FEED</span>
                  </div>

                  <div className="camera-placeholder">

                    <ScanEye size={55} />

                    <h3>Camera Feed</h3>

                    <p>
                      AI-powered video monitoring will appear here.
                    </p>

                    <span className="detection-ready">
                      <span></span> DETECTION ENGINE PENDING
                    </span>

                  </div>

                  <div className="camera-bottom">
                    <span>1280 × 720</span>
                    <span>YOLO11n • NOT CONNECTED</span>
                  </div>

                </div>

                <div className="camera-footer">

                  <div>
                    <Wifi size={16} />
                    <span>Camera connection pending</span>
                  </div>

                  <button
                    className="text-button"
                    onClick={() => setActive("Live Monitoring")}
                  >
                    View Monitoring <ArrowUpRight size={15} />
                  </button>

                </div>

              </div>

              {/* ALERT PANEL */}

              <div className="panel alerts-panel">

                <div className="panel-header">

                  <div>
                    <h3>Recent Incidents</h3>
                    <p>Latest detected safety violations</p>
                  </div>

                  <button
                    className="text-button"
                    onClick={() => setActive("Incidents")}
                  >
                    View All <ChevronRight size={15} />
                  </button>

                </div>

                <div className="incident-list">

                  {incidents.map((incident) => (

                    <div className="incident" key={incident.id}>

                      <div className="incident-icon">
                        <CircleAlert size={19} />
                      </div>

                      <div className="incident-info">

                        <strong>{incident.type}</strong>

                        <small>
                          {incident.camera} · {incident.time}
                        </small>

                        <span className={`severity ${incident.severity.toLowerCase()}`}>
                          {incident.severity}
                        </span>

                      </div>

                      <div className="incident-status">
                        {incident.status === "Resolved"
                          ? <CheckCircle2 size={17} />
                          : <span className="unresolved-dot"></span>}
                      </div>

                    </div>

                  ))}

                </div>

              </div>

            </section>

            {/* ANALYTICS */}

            <section className="bottom-grid">

              <div className="panel analytics-panel">

                <div className="panel-header">

                  <div>
                    <h3>Incident Analytics</h3>
                    <p>Hourly violation distribution</p>
                  </div>

                  <span className="chart-label">
                    TODAY · DEMO DATA
                  </span>

                </div>

                <div className="chart-container">

                  <ResponsiveContainer width="100%" height="100%">

                    <AreaChart data={chartData}>

                      <defs>
                        <linearGradient
                          id="incidentGradient"
                          x1="0"
                          y1="0"
                          x2="0"
                          y2="1"
                        >
                          <stop
                            offset="0%"
                            stopColor="#24d5c0"
                            stopOpacity={0.3}
                          />

                          <stop
                            offset="100%"
                            stopColor="#24d5c0"
                            stopOpacity={0}
                          />
                        </linearGradient>
                      </defs>

                      <CartesianGrid
                        strokeDasharray="3 3"
                        stroke="#252a35"
                      />

                      <XAxis
                        dataKey="time"
                        stroke="#707987"
                        tickLine={false}
                        axisLine={false}
                      />

                      <YAxis
                        stroke="#707987"
                        tickLine={false}
                        axisLine={false}
                      />

                      <Tooltip
                        contentStyle={{
                          background: "#171c26",
                          border: "1px solid #303746",
                          borderRadius: "8px",
                          color: "#fff"
                        }}
                      />

                      <Area
                        type="monotone"
                        dataKey="incidents"
                        stroke="#24d5c0"
                        strokeWidth={2}
                        fill="url(#incidentGradient)"
                      />

                    </AreaChart>

                  </ResponsiveContainer>

                </div>

              </div>

              {/* SYSTEM HEALTH */}

              <div className="panel health-panel">

                <div className="panel-header">
                  <div>
                    <h3>System Health</h3>
                    <p>Live application status</p>
                  </div>
                </div>

                {/* Frontend */}

                <div className="health-item">
                  <div>
                    <span className="health-dot green-dot"></span>
                    <strong>Frontend</strong>
                  </div>
                  <span>Online</span>
                </div>

                {/* Backend */}

                <div className="health-item">
                  <div>
                    <span className={`health-dot ${
                      systemHealth?.backend === "Online"
                        ? "green-dot"
                        : "yellow-dot"
                    }`}></span>

                    <strong>Backend</strong>
                  </div>

                  <span>
                    {systemHealth?.backend || "Connecting..."}
                  </span>
                </div>

                {/* AI Engine */}

                <div className="health-item">
                  <div>
                    <span className={`health-dot ${
                      systemHealth?.ai_engine === "Online"
                        ? "green-dot"
                        : "yellow-dot"
                    }`}></span>

                    <strong>AI Engine</strong>
                  </div>

                  <span>
                    {systemHealth?.ai_engine || "Connecting..."}
                  </span>
                </div>

                {/* Camera Service */}

                <div className="health-item">
                  <div>
                    <span className={`health-dot ${
                      systemHealth?.camera_service === "Online"
                        ? "green-dot"
                        : "yellow-dot"
                    }`}></span>

                    <strong>Camera Service</strong>
                  </div>

                  <span>
                    {systemHealth?.camera_service || "Connecting..."}
                  </span>
                </div>

                {/* Database */}

                <div className="health-item">
                  <div>
                    <span className="health-dot green-dot"></span>
                    <strong>Database</strong>
                  </div>

                  <span>
                    {systemHealth?.database || "Checking..."}
                  </span>
                </div>

                {/* GPU / PROCESSING */}

                <div className="health-item">
                  <div>
                    <span className="health-dot green-dot"></span>
                    <strong>Processing</strong>
                  </div>

                  <span>
                    {systemHealth?.gpu || "Checking..."}
                  </span>
                </div>

                <div className="health-footer">
                  <Shield size={17} />
                  SENTINEL AI SECURITY CORE
                </div>

              </div>

            </section>

            <footer>
              SENTINEL AI © 2026 · INTELLIGENT EDGE SURVEILLANCE
              <span>BUILDING A SAFER ENVIRONMENT</span>
            </footer>

          </div>

        )}

      </main>

    </div>
  );
}

function StatCard({ icon: Icon, label, value, detail, color }) {

  return (
    <div className="stat-card">

      <div className={`stat-icon ${color}`}>
        <Icon size={21} />
      </div>

      <p>{label}</p>

      <h2>{value}</h2>

      <small>{detail}</small>

    </div>
  );
}

export default App;