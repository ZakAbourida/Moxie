
import React, { useState } from "react";
import { Menu, X, LayoutDashboard, Users, Calendar, ClipboardList, Settings, BarChart2, LogOut } from "lucide-react";
import { cn } from "@/lib/utils";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const navItems = [
    { name: "Dashboard", icon: <LayoutDashboard size={20} />, href: "/" },
    { name: "Athletes", icon: <Users size={20} />, href: "/athletes" },
    { name: "Training Plans", icon: <ClipboardList size={20} />, href: "/training-plans" },
    { name: "Calendar", icon: <Calendar size={20} />, href: "#" },
    { name: "Analytics", icon: <BarChart2 size={20} />, href: "#" },
    { name: "Settings", icon: <Settings size={20} />, href: "#" },
  ];

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <div
        className={cn(
          "fixed inset-y-0 left-0 z-50 bg-sidebar text-sidebar-foreground transition-all duration-300 ease-in-out",
          sidebarOpen ? "w-64" : "w-16"
        )}
      >
        {/* Sidebar header */}
        <div className="flex items-center justify-between h-16 px-4 border-b border-sidebar-border">
          <div className={cn("flex items-center space-x-2", !sidebarOpen && "justify-center w-full")}>
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
              <span className="font-bold text-white">A</span>
            </div>
            {sidebarOpen && <span className="font-bold text-lg">Athletica</span>}
          </div>
          <button
            onClick={toggleSidebar}
            className={cn("text-white hover:bg-sidebar-accent p-1 rounded", !sidebarOpen && "hidden")}
          >
            <X size={20} />
          </button>
        </div>

        {/* Sidebar content */}
        <div className="p-4 flex flex-col h-full">
          <nav className="space-y-1 flex-1">
            {navItems.map((item) => (
              <a
                key={item.name}
                href={item.href}
                onClick={(e) => {
                  if (item.href !== "#") {
                    e.preventDefault();
                    navigate(item.href);
                  }
                }}
                className={cn(
                  "flex items-center space-x-3 px-2 py-3 rounded-md hover:bg-sidebar-accent transition-colors",
                  isActive(item.href) && "bg-sidebar-accent",
                  !sidebarOpen && "justify-center px-0"
                )}
              >
                <span>{item.icon}</span>
                {sidebarOpen && <span>{item.name}</span>}
              </a>
            ))}
          </nav>

          {/* User profile and logout */}
          <div className={cn("border-t border-sidebar-border pt-4", !sidebarOpen && "px-0")}>
            {sidebarOpen && user && (
              <div className="mb-3">
                <div className="text-sm font-medium">{user.first_name} {user.last_name}</div>
                <div className="text-xs text-sidebar-foreground/70 capitalize">{user.role}</div>
              </div>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={handleLogout}
              className={cn(
                "w-full justify-start text-sidebar-foreground hover:bg-sidebar-accent",
                !sidebarOpen && "px-2 justify-center"
              )}
            >
              <LogOut size={16} />
              {sidebarOpen && <span className="ml-2">Logout</span>}
            </Button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div
        className={cn(
          "flex-1 transition-all duration-300",
          sidebarOpen ? "ml-64" : "ml-16"
        )}
      >
        {/* Header */}
        <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-sm border-b h-16 flex items-center px-6">
          {!sidebarOpen && (
            <button onClick={toggleSidebar} className="mr-4">
              <Menu size={24} />
            </button>
          )}
          <div className="flex-1">
            <h1 className="text-xl font-semibold">Athletica Training Management</h1>
          </div>
          {user && (
            <div className="flex items-center space-x-3">
              <span className="text-sm text-muted-foreground">
                Welcome, {user.first_name}
              </span>
            </div>
          )}
        </header>

        {/* Page content */}
        <main className="p-6">{children}</main>
      </div>
    </div>
  );
};

export default Layout;
