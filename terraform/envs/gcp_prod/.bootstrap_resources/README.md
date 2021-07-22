# gcp_prod/.bootstrap_resources
## 概要
gcp_prod環境のための初期リソースとそのtfstateを格納したディレクトリ。

以下のリソースが格納されています:
- stateファイル配置用bucket
- terraformのplanとapplyを行うcloudbuild
- terraformをcloudbuildで走らせるのに必要となるgoogle project service

既存のcloudbuildに変更を加えたい場合は、権限を持つ人間が手動deployし、tfstateをcommitしてください。  
新規にcloudbuildが必要な場合は、gcp_prodに作成してください。
