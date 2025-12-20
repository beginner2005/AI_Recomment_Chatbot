// mock_orders.js
import STATUS from "../config/statusOrder.js"

// Hàm helper để tạo appliedVouchers reference (sẽ được populate sau khi insert vouchers)
export const orders = [
    {
        id: "ORD001",
        customer: "Nguyễn Văn A",
        email: "nguyenvana@example.com",
        originalTotal: 39989000,
        discount: 500000,
        total: 39489000,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-20"),
        items: [
            { productId: 119, quantity: 1, price: 5899000 }, // Apple AirPods Pro (2nd Gen)
            { productId: 105, quantity: 1, price: 2499000 }, // Apple MagSafe Battery Pack
        ],
        appliedVouchers: [
            { voucherCode: "FLASH50", discountAmount: 500000 }
        ],
        shippingAddress: "123 Đường ABC, Q1, TP.HCM",
        paymentMethod: "COD",
        note: ""
    },
    {
        id: "ORD002",
        customer: "Trần Thị B",
        email: "tranthib@example.com",
        originalTotal: 9998000,
        discount: 100000,
        total: 9898000,
        status: STATUS.DaXacNhan,
        date: new Date("2025-10-21"),
        items: [
            { productId: 119, quantity: 2, price: 5899000 }, // Apple AirPods Pro (2nd Gen)
        ],
        appliedVouchers: [
            { voucherCode: "NEWYEAR100", discountAmount: 100000 }
        ],
        shippingAddress: "456 Đường XYZ, Q2, TP.HCM",
        paymentMethod: "COD",
        note: "Giao giờ hành chính"
    },
    {
        id: "ORD003",
        customer: "Lê Minh C",
        email: "leminhc@example.com",
        originalTotal: 699700,
        discount: 50000,
        total: 649700,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-22"),
        items: [
            { productId: 104, quantity: 2, price: 199900 }, // Apple iPhone Charger
            { productId: 108, quantity: 1, price: 299900 }, // iPhone 12 Silicone Case
        ],
        appliedVouchers: [
            { voucherCode: "WELCOME50", discountAmount: 50000 }
        ],
        shippingAddress: "789 Đường DEF, Q3, TP.HCM",
        paymentMethod: "Banking",
        note: ""
    },
    {
        id: "ORD004",
        customer: "Phạm Quang D",
        email: "phamngocd@example.com",
        originalTotal: 48990000,
        discount: 1000000,
        total: 47990000,
        status: STATUS.DaXacNhan,
        date: new Date("2025-10-22"),
        items: [
            { productId: 119, quantity: 1, price: 5899000 }, // Apple AirPods Pro (2nd Gen)
        ],
        appliedVouchers: [
            { voucherCode: "TECH20", discountAmount: 1000000 }
        ],
        shippingAddress: "321 Đường GHI, Q4, TP.HCM",
        paymentMethod: "COD",
        note: "Kiểm tra kỹ trước khi nhận"
    },
    {
        id: "ORD005",
        customer: "Hoàng Thị E",
        email: "hoanganhe@example.com",
        originalTotal: 21489000,
        discount: 0,
        total: 21489000,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-23"),
        items: [
            { productId: 140, quantity: 1, price: 21489000 }, // Apple Watch Ultra 2
        ],
        appliedVouchers: [],
        shippingAddress: "654 Đường JKL, Q5, TP.HCM",
        paymentMethod: "COD",
        note: ""
    },
    {
        id: "ORD006",
        customer: "Ngô Văn F",
        email: "ngothif@example.com",
        originalTotal: 5899000,
        discount: 30000,
        total: 5869000,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-23"),
        items: [
            { productId: 119, quantity: 1, price: 5899000 }, // AirPods Pro (2nd Gen)
        ],
        appliedVouchers: [
            { voucherCode: "FREESHIP", discountAmount: 30000 }
        ],
        shippingAddress: "987 Đường MNO, Q6, TP.HCM",
        paymentMethod: "COD",
        note: ""
    },
    {
        id: "ORD007",
        customer: "Đặng Thị G",
        email: "dangminhg@example.com",
        originalTotal: 1298000,
        discount: 0,
        total: 1298000,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-24"),
        items: [
            { productId: 145, quantity: 4, price: 324500 }, // Lightning to USB Cable
        ],
        appliedVouchers: [],
        shippingAddress: "147 Đường PQR, Q7, TP.HCM",
        paymentMethod: "Banking",
        note: ""
    },
    {
        id: "ORD008",
        customer: "Bùi Minh H",
        email: "buithih@example.com",
        originalTotal: 20489000,
        discount: 800000,
        total: 19689000,
        status: STATUS.DaXacNhan,
        date: new Date("2025-10-24"),
        items: [
            { productId: 119, quantity: 1, price: 5899000 }, // AirPods Pro
            { productId: 135, quantity: 1, price: 3490000 }, // Apple Pencil (2nd Gen)
        ],
        appliedVouchers: [
            { voucherCode: "MEGA30", discountAmount: 800000 }
        ],
        shippingAddress: "258 Đường STU, Q8, TP.HCM",
        paymentMethod: "COD",
        note: ""
    },
    {
        id: "ORD009",
        customer: "Vũ Thanh I",
        email: "vuduci@example.com",
        originalTotal: 41980000,
        discount: 2000000,
        total: 39980000,
        status: STATUS.DaGiao,
        date: new Date("2025-10-25"),
        items: [
            { productId: 119, quantity: 2, price: 5899000 }, // AirPods Pro
        ],
        appliedVouchers: [
            { voucherCode: "VIP15", discountAmount: 2000000 }
        ],
        shippingAddress: "369 Đường VWX, Q9, TP.HCM",
        paymentMethod: "Banking",
        note: "Khách VIP"
    },
    {
        id: "ORD010",
        customer: "Phan Đình J",
        email: "phanthanhj@example.com",
        originalTotal: 8999000,
        discount: 200000,
        total: 8799000,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-25"),
        items: [
            { productId: 135, quantity: 1, price: 3490000 }, // Apple Pencil
        ],
        appliedVouchers: [
            { voucherCode: "WINTER200", discountAmount: 200000 }
        ],
        shippingAddress: "741 Đường YZA, Q10, TP.HCM",
        paymentMethod: "COD",
        note: ""
    },
    {
        id: "ORD011",
        customer: "Nguyễn Văn K",
        email: "nguyenhoangk@example.com",
        originalTotal: 3480000,
        discount: 348000,
        total: 3132000,
        status: STATUS.DaXacNhan,
        date: new Date("2025-10-26"),
        items: [
            { productId: 104, quantity: 1, price: 199900 }, // iPhone Charger
            { productId: 105, quantity: 1, price: 2499000 }, // MagSafe Battery
        ],
        appliedVouchers: [
            { voucherCode: "LOYALTY10", discountAmount: 348000 }
        ],
        shippingAddress: "852 Đường BCD, Q11, TP.HCM",
        paymentMethod: "COD",
        note: ""
    },
    {
        id: "ORD012",
        customer: "Trần Minh L",
        email: "tranducl@example.com",
        originalTotal: 799000,
        discount: 0,
        total: 799000,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-26"),
        items: [
            { productId: 108, quantity: 4, price: 299900 }, // iPhone Case
        ],
        appliedVouchers: [],
        shippingAddress: "963 Đường EFG, Q12, TP.HCM",
        paymentMethod: "Banking",
        note: ""
    },
    {
        id: "ORD013",
        customer: "Lê Thị M",
        email: "lethim@example.com",
        originalTotal: 25990000,
        discount: 600000,
        total: 25390000,
        status: STATUS.DaGiao,
        date: new Date("2025-10-27"),
        items: [
            { productId: 119, quantity: 1, price: 5899000 }, // AirPods Pro
        ],
        appliedVouchers: [
            { voucherCode: "XMAS25", discountAmount: 600000 }
        ],
        shippingAddress: "159 Đường HIJ, Bình Thạnh, TP.HCM",
        paymentMethod: "Banking",
        note: "Giao buổi sáng"
    },
    {
        id: "ORD014",
        customer: "Phạm Hùng N",
        email: "phamdinhn@example.com",
        originalTotal: 3999000,
        discount: 0,
        total: 3999000,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-27"),
        items: [
            { productId: 128, quantity: 2, price: 1999500 }, // Apple HomePod (2nd Gen)
        ],
        appliedVouchers: [],
        shippingAddress: "753 Đường KLM, Phú Nhuận, TP.HCM",
        paymentMethod: "COD",
        note: ""
    },
    {
        id: "ORD015",
        customer: "Hoàng Anh O",
        email: "hoangthio@example.com",
        originalTotal: 14999000,
        discount: 500000,
        total: 14499000,
        status: STATUS.DaGiao,
        date: new Date("2025-10-28"),
        items: [
            { productId: 140, quantity: 1, price: 21489000 }, // Apple Watch Ultra 2
        ],
        appliedVouchers: [
            { voucherCode: "FLASH50", discountAmount: 500000 }
        ],
        shippingAddress: "951 Đường NOP, Gò Vấp, TP.HCM",
        paymentMethod: "Banking",
        note: ""
    },
    {
        id: "ORD016",
        customer: "Ngô Thị P",
        email: "ngoducp@example.com",
        originalTotal: 1999000,
        discount: 0,
        total: 1999000,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-28"),
        items: [
            { productId: 105, quantity: 1, price: 2499000 }, // MagSafe Battery Pack
        ],
        appliedVouchers: [],
        shippingAddress: "357 Đường QRS, Tân Bình, TP.HCM",
        paymentMethod: "COD",
        note: ""
    },
    {
        id: "ORD017",
        customer: "Đặng Văn Q",
        email: "dangthiquynh@example.com",
        originalTotal: 55980000,
        discount: 2000000,
        total: 53980000,
        status: STATUS.DaXacNhan,
        date: new Date("2025-10-29"),
        items: [
            { productId: 119, quantity: 1, price: 5899000 }, // AirPods Pro
            { productId: 121, quantity: 1, price: 8999000 }, // Apple Watch SE
        ],
        appliedVouchers: [
            { voucherCode: "VIP15", discountAmount: 2000000 }
        ],
        shippingAddress: "486 Đường TUV, Tân Phú, TP.HCM",
        paymentMethod: "Banking",
        note: "Khách hàng doanh nghiệp"
    },
    {
        id: "ORD018",
        customer: "Bùi Thị R",
        email: "buitrungk@example.com",
        originalTotal: 998000,
        discount: 0,
        total: 998000,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-29"),
        items: [
            { productId: 119, quantity: 1, price: 5899000 }, // AirPods Pro
            { productId: 121, quantity: 1, price: 8999000 }, // Apple Watch SE
        ],
        appliedVouchers: [],
        shippingAddress: "642 Đường WXY, Bình Tân, TP.HCM",
        paymentMethod: "COD",
        note: ""
    },
    {
        id: "ORD019",
        customer: "Vũ Minh S",
        email: "vuthanhs@example.com",
        originalTotal: 799000,
        discount: 0,
        total: 799000,
        status: STATUS.ChoXacNhan,
        date: new Date("2025-10-30"),
        items: [
            { productId: 119, quantity: 1, price: 5899000 }, // AirPods Pro
            { productId: 121, quantity: 1, price: 8999000 }, // Apple Watch SE
        ],
        appliedVouchers: [],
        shippingAddress: "831 Đường ZAB, Củ Chi, TP.HCM",
        paymentMethod: "Banking",
        note: ""
    },
    {
        id: "ORD020",
        customer: "Phan Thị T",
        email: "phanduct@example.com",
        originalTotal: 12999000,
        discount: 100000,
        total: 12899000,
        status: STATUS.DaGiao,
        date: new Date("2025-10-30"),
        items: [
            { productId: 128, quantity: 1, price: 7999000 }, // HomePod
        ],
        appliedVouchers: [
            { voucherCode: "NEWYEAR100", discountAmount: 100000 }
        ],
        shippingAddress: "159 Đường CDE, Hóc Môn, TP.HCM",
        paymentMethod: "COD",
        note: ""
    },
];

export default orders;