with fighter_names as (
    select
        name,
        nickname
    from {{ ref('stg_fighters_raw') }}
)
select * from fighter_names