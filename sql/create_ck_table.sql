
----------------------------------------------------------------
--   Table Name: 用户文件                                           
--   Table Code: user_file
----------------------------------------------------------------
create table if not exists phy_user_file(
  user_file_id Int64,
  file_uuid Nullable(String),
  upload_user_id Nullable(Int64),
  file_name Nullable(String),
  file_type Nullable(String),
  content_type Nullable(String),
  file_storage Nullable(String),
  cdn_url Nullable(String),
  file_suffix Nullable(String),
  file_content Nullable(String),
  file_preview Nullable(String),
  file_summary Nullable(String),
  upload_time Nullable(DateTime),
  deleted Int8 default 0,
  ver_id Int64 default toYYYYMMDDhhmmss(now())%1000000000000 * 10000 + 9999,
  ver_dt DateTime MATERIALIZED now()
)ENGINE = MergeTree()
order by user_file_id
PRIMARY KEY user_file_id;


----------------------------------------------------------------
--   Table Name: 用户文件
--   Table Code: user_file
----------------------------------------------------------------
create or replace view v_user_file as
select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time
from phy_user_file
where (user_file_id,ver_id) in (select a.user_file_id,max(a.ver_id) from phy_user_file a group by user_file_id)
      and deleted = 0
order by user_file_id desc;

----------------------------------------------------------------
--   Table Name: 用户文件
--   Table Code: user_file
----------------------------------------------------------------
create or replace view vs_user_file as
select t.user_file_id user_file_id, t.file_uuid file_uuid, t.upload_user_id upload_user_id, t.file_name file_name, t.file_type file_type, t.content_type content_type, t.file_storage file_storage, t.cdn_url cdn_url, t.file_suffix file_suffix, t.file_content file_content, t.file_preview file_preview, t.file_summary file_summary, t.upload_time upload_time
        ,(mr1.sys_user_id, mr1.user_name, mr1.pwd, mr1.last_login_time, mr1.last_active_time, mr1.create_time, mr1.update_time, mr1.last_login_info, mr1.remark) ref_UploadUserId_SysUser
from v_user_file t
        left join v_sys_user mr1 on mr1.sys_user_id = t.upload_user_id
order by t.user_file_id desc;