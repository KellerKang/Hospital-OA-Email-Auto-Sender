# 医院业务流程和信息系统UML图

## 医院整体业务流程和信息系统架构图

```mermaid
graph TB
    %% 患者入口
    Patient[患者] --> Registration[挂号系统]
    Patient --> Emergency[急诊系统]
    
    %% 挂号流程
    Registration --> Appointment[预约管理]
    Registration --> Payment[收费系统]
    Appointment --> Schedule[排班系统]
    
    %% 急诊流程
    Emergency --> Triage[分诊系统]
    Triage --> EmergencyCare[急诊救治]
    EmergencyCare --> Admission[住院系统]
    
    %% 门诊流程
    Registration --> Outpatient[门诊系统]
    Outpatient --> MedicalRecord[电子病历系统]
    Outpatient --> Lab[检验系统]
    Outpatient --> Imaging[影像系统]
    Outpatient --> Pharmacy[药房系统]
    
    %% 住院流程
    Admission --> Ward[病房管理]
    Ward --> Nursing[护理系统]
    Ward --> MedicalRecord
    Ward --> Lab
    Ward --> Imaging
    Ward --> Pharmacy
    
    %% 医疗核心系统
    MedicalRecord --> Diagnosis[诊断系统]
    MedicalRecord --> Treatment[治疗系统]
    MedicalRecord --> Prescription[处方系统]
    
    %% 医技科室
    Lab --> LabResult[检验结果]
    Imaging --> ImageResult[影像结果]
    LabResult --> MedicalRecord
    ImageResult --> MedicalRecord
    
    %% 药房系统
    Prescription --> Pharmacy
    Pharmacy --> Inventory[库存管理]
    Pharmacy --> DrugInfo[药品信息]
    
    %% 财务系统
    Payment --> Finance[财务系统]
    Finance --> Insurance[医保系统]
    Finance --> Billing[账单系统]
    
    %% 管理支持系统
    Schedule --> HR[人事系统]
    HR --> Staff[员工管理]
    Inventory --> Supply[物资管理]
    Supply --> Procurement[采购系统]
    
    %% 质量管理系统
    MedicalRecord --> Quality[质量管理]
    Quality --> Audit[审计系统]
    Quality --> Statistics[统计分析]
    
    %% 信息系统基础设施
    Network[网络系统] --> AllSystems[所有系统]
    Security[安全系统] --> AllSystems
    Backup[备份系统] --> AllSystems
    
    %% 样式定义
    classDef patientClass fill:#e1f5fe
    classDef systemClass fill:#f3e5f5
    classDef processClass fill:#e8f5e8
    classDef dataClass fill:#fff3e0
    
    class Patient patientClass
    class Registration,Outpatient,Emergency,Admission,Ward processClass
    class MedicalRecord,Lab,Imaging,Pharmacy,Finance,HR systemClass
    class LabResult,ImageResult,Prescription dataClass
```

## 详细业务流程时序图

```mermaid
sequenceDiagram
    participant P as 患者
    participant R as 挂号系统
    participant MR as 电子病历
    participant D as 医生
    participant L as 检验科
    participant I as 影像科
    participant PH as 药房
    participant F as 财务系统
    
    P->>R: 挂号
    R->>MR: 创建病历
    R->>F: 收费
    
    P->>D: 就诊
    D->>MR: 查看病历
    D->>L: 开检验单
    D->>I: 开影像单
    D->>PH: 开处方
    
    L->>MR: 上传检验结果
    I->>MR: 上传影像结果
    D->>MR: 更新诊断
    
    PH->>F: 药品费用
    F->>P: 结算
```

## 医院信息系统架构图

```mermaid
graph LR
    subgraph "前端层"
        Web[Web界面]
        Mobile[移动端]
        Desktop[桌面端]
    end
    
    subgraph "应用层"
        HIS[HIS系统]
        LIS[LIS系统]
        PACS[PACS系统]
        EMR[EMR系统]
        PIS[药房系统]
    end
    
    subgraph "数据层"
        DB1[(主数据库)]
        DB2[(备份数据库)]
        File[文件存储]
    end
    
    subgraph "基础设施层"
        Server[服务器]
        Network[网络]
        Security[安全]
    end
    
    Web --> HIS
    Mobile --> HIS
    Desktop --> HIS
    
    HIS --> LIS
    HIS --> PACS
    HIS --> EMR
    HIS --> PIS
    
    LIS --> DB1
    PACS --> File
    EMR --> DB1
    PIS --> DB1
    
    DB1 --> DB2
    DB1 --> Server
    File --> Server
    Server --> Network
    Network --> Security
```

## 主要业务流程说明

### 1. 患者就诊流程
- **挂号** → **分诊** → **就诊** → **检查** → **诊断** → **治疗** → **取药** → **结算**

### 2. 住院流程
- **入院** → **病房分配** → **治疗** → **护理** → **检查** → **用药** → **出院** → **结算**

### 3. 急诊流程
- **急诊挂号** → **分诊** → **紧急救治** → **检查** → **治疗** → **住院/出院**

### 4. 医技科室流程
- **接收申请** → **检查** → **结果录入** → **报告生成** → **结果推送**

### 5. 药房流程
- **接收处方** → **审核** → **配药** → **发药** → **库存更新**

### 6. 财务流程
- **收费** → **医保结算** → **账单生成** → **财务报表**

## 系统集成关系

- **HIS系统**：医院信息系统的核心，管理患者信息和业务流程
- **EMR系统**：电子病历系统，存储和管理患者医疗记录
- **LIS系统**：实验室信息系统，管理检验流程和结果
- **PACS系统**：影像归档和通信系统，管理医学影像
- **PIS系统**：药房信息系统，管理药品和处方
- **财务系统**：管理医院财务和收费
- **人事系统**：管理医院员工信息
- **物资系统**：管理医院物资和采购 