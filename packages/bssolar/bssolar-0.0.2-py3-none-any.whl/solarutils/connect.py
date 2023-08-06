# Solar A3 CTQCTP TNT Line Only!
# config.py는 AWS SECRET KEY 노출을 막기 위해 git, pypi에 upload하지 않습니다.
# set_options 함수를 사용하여 AWS KEY 설정하시거나 분석환경의 환경변수 AWS_ACCESS_KEY_ID와 AWS_SECRET_ACCESS_KEY를 설정하세요.

import os, json
import s3fs
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import dask.dataframe as dd

if os.path.exists('config.py'):
    import config
    local_config = {
        'key': config.AWS_ACCESS_KEY_ID, 
        'secret': config.AWS_SECRET_ACCESS_KEY,
    }
else:
    local_config = False

    
#### SET PACKAGE VARIABLES
ROOT = 'manufacturing-file-storage/solar-data/A3/CTQCTP_TNT_daily'


################################
## get_s3_options
################################
def get_s3_options():
    '''
    현재 지정된 s3_options(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)를 반환
    '''
    
    # load s3_options
    # Distributed 계산에서는 local_config를 사용해야 함
    if local_config is not None:
        s3_options = local_config
    else:
        s3_options = {
            'key': os.getenv('AWS_ACCESS_KEY_ID'),
            'secret': os.getenv('AWS_SECRET_ACCESS_KEY'),
        }
        
    # check s3_options exists
    for k, v in s3_options.items():
        nones = []
        if v is None:
            nones.append(k)    
    if len(nones) > 0:
        print("[WARNING] No AWS S3 Key found! Execute 'set_s3_options(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)'")
        return None
        
    return s3_options


################################
## set_s3_options
################################
def set_s3_options(aws_access_key_id, aws_secret_access_key, save_local_config=False):
    '''
    s3_options(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)를 지정
    '''
    
    # write keys
    os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
    
    # print result
    chk = get_s3_options()
    for k, v in chk.items():
        print(f"{k}: {v}")

        
################################
## get_bucket
################################
def get_bucket():
    '''
    AWS S3 버킷을 반환
    '''
    
    # get S3_options
    s3_options = get_s3_options()
    if s3_options is None:
        return None
    
    # get bucket and return
    try:
        return s3fs.S3FileSystem(**s3_options)
    except Exception as ex:
        print(f'[ERROR] {ex}')
        return None
    
        
################################
## date_to_path
################################
def date_to_path(dt, dt_end=None, n_days=None, verbose=True):
    '''
    Convert date (date range) to the filepaths in the solar bucket.
    
    Args:
      dt       <str> or <datetime> datetime (start if dt_end is given)
      dt_end   <str> or <datetime> datetime (end)
      n_days   <int> n_days 개의 파일경로 반환 (dt_end는 무시됨)
      verbose  <bool> verbose
      
    Examples:
      >>> date_to_path('2020-11-01', '2020-11-05')
      
    Return:
      filepaths in the solar bucket <list>
    '''
    
    # init
    bucket = get_bucket()
    
    # parse dt, dt_end
    if not isinstance(dt, datetime):
        dt = datetime.fromisoformat(dt)
        
    if n_days is None:
        n_days = (datetime.now() - dt).days
        if dt_end is None:
            dt_end = dt
    else:
        dt_end = datetime.now()
            
    if not isinstance(dt_end, datetime):
        dt_end = datetime.fromisoformat(dt_end)
        
    # check file exists and append paths
    filepaths = []
    while dt <= dt_end:
        fp = os.path.join(ROOT, f"year={dt.year:04}/month={dt.month:02}/{dt.year:04}-{dt.month:02}-{dt.day:02}.parquet")
        if bucket.exists(fp):
            filepaths.append(fp)
        dt += timedelta(days=1)
        if len(filepaths) >= n_days:
            break
            
    if verbose:
        print(f"Files Found:")
        n_files = len(filepaths)
        print(f"  - {n_files} files found: {filepaths[0].rsplit('/', 1)[-1]}", end=" ")
        if n_files > 1:
            print(f"to {filepaths[-1].rsplit('/', 1)[-1]}")
        else:
            print("")
    
    # linebreak
    if verbose:
        print("")
    
    return filepaths


################################
## date_to_path
################################
def list_files(dt, dt_end=None, n_days=None, verbose=False):
    '''
    지정된 기간 사이에 있는 parquet 파일 및 각 파일의 크기를 반환
    
    Args:
      dt       <str> or <datetime> datetime (start if dt_end is given)
      dt_end   <str> or <datetime> datetime (end)
      n_days   <int> n_days 개의 파일경로 반환 (dt_end는 무시됨)
      
    Examples:
      >>> list_files('2020-11-01', '2020-11-05')
      
    Return:
      list of prepared parquet files <Pandas.DataFrame>
    '''
    # init
    bucket = get_bucket()
    
    filepaths = date_to_path(dt=dt, dt_end=dt_end, n_days=n_days, verbose=verbose)
    
    info = pd.DataFrame({
        'date': [datetime.fromisoformat(f.rsplit('/', 1)[-1].rsplit('.', 1)[0]) for f in filepaths],
        'filepath': [f.replace(ROOT, '') for f in filepaths],
        'size_MB': [round(bucket.size(f)/1024/1024, 1) for f in filepaths]
    })
    
    return info


################################
## load_data
################################
def load_data(dt, dt_end=None, n_days=None, download=False, download_dir='./data', verbose=True, compute=False):
    '''
    날짜 dt와 dt_end 사이의 데이터를 S3 bucket에서 찾아 dask.dataframe으로 반환 (또는 날짜 dt부터 n_days 개의 데이터를 찾아 반환)
    S3 엑세스는 비용이 발생함으로 download=True를 권장 (로컬 디스크에서 로드하는 것이 분석 속도도 상대적으로 빠름 - Dask의 경우)
    
    Args:
      dt             <str> or <datetime> 시작 날짜
      dt_end         <str> or <datetime> 종료 날짜
      n_days         <int> 파일 갯수
      download       <bool> 다운로드 여부 - True이면 로컬 디스크에 데이터를 받은 뒤, 로컬 디스크에 위치한 parquet를 로드 (권장)
      download_dir   <str> 다운로드 경로 - 여러 사람이 함께 쓰는 호트에 다운로드 받을 때에는 공유 폴더 경로롤 지정하는 것 권장
      verbose        <bool> 진행 상황 출력
      compute        <bool> True이면 compute한 뒤 pd.DataFrame을 반환 - 시간 오래 걸림
      
    Examples:
      >>> load(data('2020-11-01', '2020-11-07', download=True))
      
    Return:
      solar CTQCTP_TNT data <daks.dataframe>
    '''
    
    # load s3_options
    s3_options = get_s3_options()
    if s3_options is None:
        print("[EXIT] Set AWS S3 Key and Secret Key First!")
        return
    
    # get paths
    fpaths = date_to_path(dt, dt_end=dt_end, n_days=n_days, verbose=verbose)

    # download
    local_fpaths = []
    if download:
        bucket = get_bucket()
        if verbose:
            print(f"Download Parquet From S3...", end=" ")
        for i, f in enumerate(fpaths):
            if verbose:
                print(f"{len(fpaths)-i}", end=", ")
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
                os.chmod(download_dir, 0o775)
            dst = os.path.join(download_dir, f.rsplit('/', 1)[-1])
            local_fpaths.append(dst)
            if not os.path.exists(dst):
                bucket.get(f, dst)
        if verbose:
            print("Done!\n")
        # set fpaths
        fpaths = local_fpaths
    else:
        fpaths = [f"s3://{s}" for s in fpaths]
    
    # read parquets
    if verbose:
        print(f"Loading Parquets...", end=" ")
    df = dd.read_parquet(fpaths, engine='pyarrow', storage_options=s3_options)
    if verbose:
        print("Done!\n")
    
    # compute
    if compute:
        if verbose:
            print(f"Dask.DataFrame to Pandas.DataFrame (takes a long time)...", end=" ")
        df = df.compute()
        if verbose:
            print("Done!\n")
        
    return df
