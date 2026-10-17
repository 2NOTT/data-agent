SET NAMES utf8mb4;
CREATE DATABASE IF NOT EXISTS dw_edu DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE dw_edu;

-- 仅供空数据库首次初始化，保留已有表和数据。
CREATE TABLE dim_course (
    course_id VARCHAR(20) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    level VARCHAR(20) NOT NULL
);

CREATE TABLE dim_campus (
    campus_id VARCHAR(20) PRIMARY KEY,
    campus_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL
);

CREATE TABLE dim_student (
    student_id VARCHAR(20) PRIMARY KEY,
    student_type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    campus_id VARCHAR(20) NOT NULL
);

CREATE TABLE fact_enrollment (
    enrollment_id VARCHAR(30) PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    course_id VARCHAR(20) NOT NULL,
    campus_id VARCHAR(20) NOT NULL,
    enrollment_date DATE NOT NULL,
    status_code VARCHAR(20) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    completed_sessions INT NOT NULL,
    total_sessions INT NOT NULL
);

INSERT INTO dim_course VALUES
('C001', 'Python数据分析', '数据分析', '入门'),
('C002', 'RAG应用开发', '人工智能', '进阶'),
('C003', 'Java后端基础', '编程开发', '入门'),
('C004', 'LangGraph智能体实战', '人工智能', '进阶'),
('C005', 'SQL数据分析', '数据分析', '入门');

INSERT INTO dim_campus VALUES
('CA001', '广州校区', '广州'),
('CA002', '深圳校区', '深圳'),
('CA003', '线上学习中心', '线上');

INSERT INTO dim_student VALUES
('S001', '学生', '女', 'CA001'), ('S002', '成人', '男', 'CA002'),
('S003', '学生', '男', 'CA001'), ('S004', '企业客户', '女', 'CA003'),
('S005', '成人', '女', 'CA002'), ('S006', '学生', '女', 'CA001'),
('S007', '成人', '男', 'CA003'), ('S008', '企业客户', '男', 'CA003');

INSERT INTO fact_enrollment VALUES
('E20260101001', 'S001', 'C001', 'CA001', '2026-01-03', 'completed', 1999, 10, 10),
('E20260102001', 'S002', 'C002', 'CA002', '2026-01-05', 'active', 2999, 8, 12),
('E20260103001', 'S003', 'C003', 'CA001', '2026-01-08', 'completed', 1799, 9, 10),
('E20260104001', 'S004', 'C004', 'CA003', '2026-01-10', 'active', 3999, 6, 12),
('E20260105001', 'S005', 'C005', 'CA002', '2026-01-12', 'completed', 1299, 8, 8),
('E20260106001', 'S006', 'C001', 'CA001', '2026-02-02', 'active', 1999, 7, 10),
('E20260107001', 'S007', 'C002', 'CA003', '2026-02-05', 'active', 2999, 5, 12),
('E20260108001', 'S008', 'C004', 'CA003', '2026-02-08', 'completed', 3999, 12, 12),
('E20260109001', 'S001', 'C005', 'CA001', '2026-02-15', 'refunded', 1299, 0, 8),
('E20260110001', 'S003', 'C001', 'CA001', '2026-03-01', 'active', 1999, 4, 10),
('E20260111001', 'S005', 'C003', 'CA002', '2026-03-04', 'active', 1799, 3, 10),
('E20260112001', 'S007', 'C005', 'CA003', '2026-03-06', 'completed', 1299, 8, 8);
