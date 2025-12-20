import ROLE from "../config/role.js";
const users = [
    {
        email: "admin@exclusive.com",
        username: "Admin",
        password: "binhdeptrai",
        dob: new Date("1996-09-01"),
        address: "2 Lê Thánh Tôn, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.ADMIN,
        avatar: "https://randomuser.me/api/portraits/men/10.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "VIP15", claimedAt: new Date("2024-12-15"), isUsed: true },
            { voucherCode: "MEGA30", claimedAt: new Date("2024-12-20"), isUsed: false },
        ]
    },
    {
        email: "nguyenvana@example.com",
        username: "Nguyễn Văn A",
        password: "12345678",
        dob: new Date("1995-06-12"),
        address: "123 Lê Lợi, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/11.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "FLASH50", claimedAt: new Date("2025-01-01"), isUsed: true },
            { voucherCode: "LOYALTY10", claimedAt: new Date("2025-01-05"), isUsed: false },
        ]
    },
    {
        email: "tranthib@example.com",
        username: "Trần Thị B",
        password: "12345678",
        dob: new Date("1998-03-25"),
        address: "45 Nguyễn Huệ, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/22.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "NEWYEAR100", claimedAt: new Date("2025-01-01"), isUsed: true },
        ]
    },
    {
        email: "leminhc@example.com",
        username: "Lê Minh C",
        password: "12345678",
        dob: new Date("1990-10-10"),
        address: "56 Hai Bà Trưng, Quận 3, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/33.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "WELCOME50", claimedAt: new Date("2024-12-28"), isUsed: true },
            { voucherCode: "TECH20", claimedAt: new Date("2025-01-03"), isUsed: false },
        ]
    },
    {
        email: "phamngocd@example.com",
        username: "Phạm Ngọc D",
        password: "12345678",
        dob: new Date("1992-12-05"),
        address: "12 Nguyễn Văn Cừ, Quận 5, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/44.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "TECH20", claimedAt: new Date("2025-01-02"), isUsed: true },
        ]
    },
    {
        email: "hoanganhe@example.com",
        username: "Hoàng Anh E",
        password: "12345678",
        dob: new Date("1988-08-18"),
        address: "22 Phan Xích Long, Phú Nhuận, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/55.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "ngothif@example.com",
        username: "Ngô Thị F",
        password: "12345678",
        dob: new Date("1999-04-09"),
        address: "7 Bạch Đằng, Bình Thạnh, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/66.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "FREESHIP", claimedAt: new Date("2025-01-04"), isUsed: true },
            { voucherCode: "XMAS25", claimedAt: new Date("2024-12-24"), isUsed: false },
        ]
    },
    {
        email: "dangminhg@example.com",
        username: "Đặng Minh G",
        password: "12345678",
        dob: new Date("1993-02-14"),
        address: "88 Cách Mạng Tháng 8, Quận 10, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/77.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "buithih@example.com",
        username: "Bùi Thị H",
        password: "12345678",
        dob: new Date("2000-01-10"),
        address: "34 Pasteur, Quận 3, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/88.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "MEGA30", claimedAt: new Date("2025-01-01"), isUsed: true },
        ]
    },
    {
        email: "vuduci@example.com",
        username: "Vũ Đức I",
        password: "12345678",
        dob: new Date("1985-11-23"),
        address: "5 Võ Văn Kiệt, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/99.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "VIP15", claimedAt: new Date("2025-01-02"), isUsed: true },
        ]
    },
    {
        email: "phanthanhj@example.com",
        username: "Phan Thanh J",
        password: "12345678",
        dob: new Date("1996-09-01"),
        address: "2 Lê Thánh Tôn, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/10.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "WINTER200", claimedAt: new Date("2024-12-22"), isUsed: true },
        ]
    },
    // --- Bổ sung thêm 30 users ---
    {
        email: "nguyenhoangk@example.com",
        username: "Nguyễn Hoàng K",
        password: "12345678",
        dob: new Date("1994-07-20"),
        address: "15 Sư Vạn Hạnh, Quận 10, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/1.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "LOYALTY10", claimedAt: new Date("2025-01-03"), isUsed: true },
        ]
    },
    {
        email: "tranducl@example.com",
        username: "Trần Đức L",
        password: "12345678",
        dob: new Date("1991-05-30"),
        address: "18 Phạm Ngũ Lão, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/2.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "lethim@example.com",
        username: "Lê Thị M",
        password: "12345678",
        dob: new Date("1997-01-15"),
        address: "33 Nguyễn Trãi, Quận 5, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/3.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "XMAS25", claimedAt: new Date("2024-12-25"), isUsed: true }
        ]
    },
    {
        email: "phamdinhn@example.com",
        username: "Phạm Đình N",
        password: "12345678",
        dob: new Date("1986-11-03"),
        address: "10 Đồng Khởi, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/4.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "hoangthio@example.com",
        username: "Hoàng Thị O",
        password: "12345678",
        dob: new Date("2001-08-22"),
        address: "99 Vạn Kiếp, Bình Thạnh, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/5.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "FLASH50", claimedAt: new Date("2025-01-06"), isUsed: true },
            { voucherCode: "FREESHIP", claimedAt: new Date("2025-01-07"), isUsed: true }
        ]
    },
    {
        email: "ngoducp@example.com",
        username: "Ngô Đức P",
        password: "12345678",
        dob: new Date("1995-04-16"),
        address: "44 Đinh Tiên Hoàng, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/6.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "dangthiquynh@example.com",
        username: "Đặng Thị Q",
        password: "12345678",
        dob: new Date("1990-02-28"),
        address: "50 Nguyễn Thị Minh Khai, Quận 3, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/7.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "buitrungk@example.com",
        username: "Bùi Trung R",
        password: "12345678",
        dob: new Date("1989-12-19"),
        address: "100 Phan Đình Phùng, Phú Nhuận, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/8.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "VIP15", claimedAt: new Date("2025-01-04"), isUsed: true }
        ]
    },
    {
        email: "vuthanhs@example.com",
        username: "Vũ Thanh S",
        password: "12345678",
        dob: new Date("1998-06-07"),
        address: "20 Lý Tự Trọng, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/9.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "phanduct@example.com",
        username: "Phan Đức T",
        password: "12345678",
        dob: new Date("1993-10-02"),
        address: "55 Hùng Vương, Quận 5, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/12.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "TECH20", claimedAt: new Date("2025-01-05"), isUsed: true }
        ]
    },
    {
        email: "nguyenvanu@example.com",
        username: "Nguyễn Văn U",
        password: "12345678",
        dob: new Date("1996-03-17"),
        address: "77 Nguyễn Văn Thủ, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/13.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "VIP15", claimedAt: new Date("2025-01-06"), isUsed: true }
        ]
    },
    {
        email: "tranvantranv@example.com",
        username: "Trần Văn V",
        password: "12345678",
        dob: new Date("1987-09-08"),
        address: "123 Đinh Bộ Lĩnh, Bình Thạnh, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/14.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "FREESHIP", claimedAt: new Date("2025-01-07"), isUsed: true }
        ]
    },
    {
        email: "lethuyw@example.com",
        username: "Lê Thúy W",
        password: "12345678",
        dob: new Date("2000-11-25"),
        address: "333 Võ Văn Tần, Quận 3, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/15.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "phamxuanx@example.com",
        username: "Phạm Xuân X",
        password: "12345678",
        dob: new Date("1994-01-01"),
        address: "44 Cộng Hòa, Tân Bình, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/16.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "hoanghaimy@example.com",
        username: "Hoàng Hải Y",
        password: "12345678",
        dob: new Date("1992-05-04"),
        address: "55 Trường Chinh, Quận 12, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/17.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "WINTER200", claimedAt: new Date("2024-12-25"), isUsed: true }
        ]
    },
    {
        email: "ngoduongz@example.com",
        username: "Ngô Dương Z",
        password: "12345678",
        dob: new Date("1985-07-11"),
        address: "66 Lý Thường Kiệt, Tân Bình, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/18.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "danghoanga1@example.com",
        username: "Đặng Hoàng A1",
        password: "12345678",
        dob: new Date("1999-09-09"),
        address: "11 Mạc Thị Bưởi, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/19.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "buitranga2@example.com",
        username: "Bùi Trang A2",
        password: "12345678",
        dob: new Date("1991-04-29"),
        address: "22 Trần Hưng Đạo, Quận 5, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/20.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "NEWYEAR100", claimedAt: new Date("2025-01-01"), isUsed: true }
        ]
    },
    {
        email: "vuminha3@example.com",
        username: "Vũ Minh A3",
        password: "12345678",
        dob: new Date("1988-12-12"),
        address: "33 Cao Thắng, Quận 3, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/21.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "phanquanga4@example.com",
        username: "Phan Quang A4",
        password: "12345678",
        dob: new Date("1995-02-05"),
        address: "44 Hoàng Diệu, Quận 4, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/23.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "nguyenthia5@example.com",
        username: "Nguyễn Thị A5",
        password: "12345678",
        dob: new Date("1997-10-28"),
        address: "55 Vĩnh Viễn, Quận 10, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/24.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "WELCOME50", claimedAt: new Date("2025-01-08"), isUsed: true }
        ]
    },
    {
        email: "tranhunga6@example.com",
        username: "Trần Hùng A6",
        password: "12345678",
        dob: new Date("1990-08-01"),
        address: "66 Nguyễn Đình Chiểu, Quận 3, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/25.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "lehoanga7@example.com",
        username: "Lê Hoàng A7",
        password: "12345678",
        dob: new Date("1986-06-20"),
        address: "77 Nguyễn Văn Trỗi, Phú Nhuận, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/26.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "TECH20", claimedAt: new Date("2025-01-09"), isUsed: true }
        ]
    },
    {
        email: "phamthanhnga8@example.com",
        username: "Phạm Thanh A8",
        password: "12345678",
        dob: new Date("2001-03-03"),
        address: "88 Điện Biên Phủ, Bình Thạnh, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/27.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "hoangminha9@example.com",
        username: "Hoàng Minh A9",
        password: "12345678",
        dob: new Date("1993-11-14"),
        address: "99 Hai Bà Trưng, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/28.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "ngoconga10@example.com",
        username: "Ngô Công A10",
        password: "12345678",
        dob: new Date("1989-01-27"),
        address: "10 Phan Văn Trị, Gò Vấp, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/29.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "dangthiba11@example.com",
        username: "Đặng Thị A11",
        password: "12345678",
        dob: new Date("1996-05-18"),
        address: "11 Võ Văn Kiệt, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/30.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "MEGA30", claimedAt: new Date("2025-01-10"), isUsed: true }
        ]
    },
    {
        email: "buihoanga12@example.com",
        username: "Bùi Hoàng A12",
        password: "12345678",
        dob: new Date("1994-07-07"),
        address: "12 Nguyễn Thị Thập, Quận 7, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/31.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "vuthia13@example.com",
        username: "Vũ Thị A13",
        password: "12345678",
        dob: new Date("1987-04-24"),
        address: "13 Lạc Long Quân, Quận 11, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/32.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "XMAS25", claimedAt: new Date("2024-12-26"), isUsed: true }
        ]
    },
    {
        email: "phamlama14@example.com",
        username: "Phạm Lâm A14",
        password: "12345678",
        dob: new Date("1998-10-06"),
        address: "14 Pasteur, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/men/34.jpg",
        isVerified: true,
        vouchers: []
    },
    {
        email: "nguyenthunga15@example.com",
        username: "Nguyễn Thư A15",
        password: "12345678",
        dob: new Date("1992-02-14"),
        address: "15 Lê Thánh Tôn, Quận 1, TP. Hồ Chí Minh",
        role: ROLE.USER,
        avatar: "https://randomuser.me/api/portraits/women/35.jpg",
        isVerified: true,
        vouchers: [
            { voucherCode: "FLASH50", claimedAt: new Date("2025-01-11"), isUsed: true }
        ]
    },
];

export default users;