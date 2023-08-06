import os,django
from django.conf import settings
# 加载django配置
current_dir=os.getcwd()
setting_model_str=current_dir.split("\\")[-1]+".settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_model_str)
django.setup()
# your imports, e.g. Django models
from c_mssql import DB_Config
from c_mssql.mssql_conn import Mssql_Conn


def add_sql_description(table_name,column_name,description):
    sql_str=f"""
IF EXISTS(
SELECT top 1 1
FROM sys.tables AS t
INNER JOIN sys.columns
AS c ON t.object_id = c.object_id
inner JOIN sys.extended_properties AS ep
ON ep.major_id = c.object_id AND ep.minor_id = c.column_id and ep.class =1
WHERE 1=1
AND t.name='{table_name}' 
AND C.name= '{column_name}'
AND EP.class=1
)
BEGIN
EXEC sp_updateextendedproperty   
@name = N'MS_Description',   
@value = '{description}',  
@level0type = N'Schema', @level0name = 'dbo',  
@level1type = N'Table',  @level1name = '{table_name}',  
@level2type = N'Column', @level2name = '{column_name}'; 
END
ELSE
BEGIN
EXEC sp_addextendedproperty   
@name = N'MS_Description',   
@value = '{description}',  
@level0type = N'Schema', @level0name = 'dbo',  
@level1type = N'Table',  @level1name = '{table_name}',  
@level2type = N'Column', @level2name = '{column_name}'; 
END
 
"""
    server=settings.DATABASES["default"]["HOST"]
    database=settings.DATABASES["default"]["NAME"]
    username=settings.DATABASES["default"]["USER"]
    password=settings.DATABASES["default"]["PASSWORD"]
    conn=Mssql_Conn(DB_Config(server,database,username,password))
    conn.open()
    conn.execute(sql_str)
    conn.commit()
    conn.close()


def update_MS_Description(models):
    data_list=[]
    for key in dir(models):
        model=getattr(models,key)
        try:
            if model.__module__=="project.models":
                model_name=key
                model=model
                table_name=model.__dict__["_meta"].db_table
                filed_str=model.__doc__
                filed_str=filed_str[len(model_name)+1:len(filed_str)-1]
                for field in filed_str.split(","):
                    field=field.strip()
                    filed_tmp=getattr(model,field)
                    field_name=filed_tmp.field.db_column if bool(filed_tmp.field.db_column) else field
                    verbose_name=filed_tmp.field.verbose_name
                    if field_name!=verbose_name:
                        row_dict={"table_name":table_name,"field_name":field_name,"verbose_name":verbose_name}
                        if row_dict not in data_list:
                            data_list.append(row_dict)
        except:
            pass

    for row_dict in data_list:
        print("正在更新:",row_dict)
        add_sql_description(row_dict["table_name"],row_dict["field_name"],row_dict["verbose_name"])
    print("更新成功")
    