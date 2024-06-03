import React, { useState } from "react";
import ProfilePic from "../ProfilePic";
import { Tooltip, Menu, MenuItem, Typography } from "@mui/material";
import useAuth, { useUserDetails } from "../../../hooks/useAuth";
import { useNavigate } from "react-router-dom";

const ProfileMenu: React.FC = () => {
    const [tooltipOpen, setTooltipOpen] = useState(false);
    const [menuAnchor, setMenuAnchor] = useState<null | HTMLElement>(null);
    const { userName } = useUserDetails();
    const navigate = useNavigate();

    const handleTooltipOpen = () => {
        setTooltipOpen(true);
    };

    const handleTooltipClose = () => {
        setTooltipOpen(false);
    };

    const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
        setMenuAnchor(event.currentTarget);
    };

    const handleMenuClose = () => {
        setMenuAnchor(null);
    };

    const handleLogOut = () => {
        window.localStorage.removeItem("token");
        navigate("/login");
    }

    return (
        <>
            <Tooltip
                open={tooltipOpen}
                onClose={handleTooltipClose}
                onOpen={handleTooltipOpen}
                title={userName}
            >
                <div onClick={handleMenuOpen}>
                    <ProfilePic />
                </div>
            </Tooltip>
            <Menu
                anchorEl={menuAnchor}
                open={Boolean(menuAnchor)}
                onClose={handleMenuClose}
            >
                <MenuItem style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '1rem'
                }}>
                    <Typography variant="body1">{userName}</Typography>
                    <ProfilePic />
                </MenuItem>
                <MenuItem onClick={handleLogOut}>Sign Out</MenuItem>
            </Menu>
        </>
    );
};

export default ProfileMenu;
