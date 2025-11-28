import { useState } from "react";
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
} from "@mui/material";
import { Dashboard as DashboardIcon, Analytics as AnalyticsIcon, Menu as MenuIcon } from "@mui/icons-material";

const drawerWidth = 240;

interface LayoutProps {
  children: React.ReactNode;
  currentView: "overview" | "analyzer";
  onViewChange: (view: "overview" | "analyzer") => void;
}

export const Layout = ({ children, currentView, onViewChange }: LayoutProps) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <div>
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{
            color: "#1976d2",
            fontWeight: "bold",
            fontSize: "1.1rem",
            lineHeight: 1.2,
            wordWrap: "break-word",
          }}
        >
          VORTEX Dashboard
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        <ListItem disablePadding>
          <ListItemButton selected={currentView === "overview"} onClick={() => onViewChange("overview")}>
            <ListItemIcon>
              <DashboardIcon color={currentView === "overview" ? "primary" : "inherit"} />
            </ListItemIcon>
            <ListItemText primary="Resumen General" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton selected={currentView === "analyzer"} onClick={() => onViewChange("analyzer")}>
            <ListItemIcon>
              <AnalyticsIcon color={currentView === "analyzer" ? "primary" : "inherit"} />
            </ListItemIcon>
            <ListItemText primary="Analizar Ticket" />
          </ListItemButton>
        </ListItem>
      </List>
    </div>
  );

  return (
    <Box sx={{ display: "flex" }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: "none" } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            {currentView === "overview" ? "Resumen del Sistema" : "Análisis Inteligente de Tickets"}
          </Typography>
        </Toolbar>
      </AppBar>
      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: "block", sm: "none" },
            "& .MuiDrawer-paper": { boxSizing: "border-box", width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: "none", sm: "block" },
            "& .MuiDrawer-paper": { boxSizing: "border-box", width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` }, mt: 8 }}>
        {children}
      </Box>
    </Box>
  );
};
