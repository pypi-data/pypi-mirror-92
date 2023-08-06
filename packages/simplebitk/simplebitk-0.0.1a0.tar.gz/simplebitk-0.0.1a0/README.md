# BioInformatics Tools kit
> Summarized some useful tools in it.


BITK will help us manipulate data in different formats.

## Install

`pip install bitk`

## How to use

### dedim.py



```bash
usage: dedim.py [-h] [--sep SEP] [--dedimensions-method DEDIMENSIONS_METHOD]
                [--cluster-method CLUSTER_METHOD]
                [--assess-method ASSESS_METHOD] [--dimensions DIMENSIONS]
                [--cluster-number CLUSTER_NUMBER] [-r] [--no-row-feature]
                [--annotation ANNOTATION] [--size SIZE] [--style STYLE]
                [-t TITLE] [-f FIG] [--version]
                matrix prefix

positional arguments:
  matrix                matrix table, if row represents feature, please note to add '--row-feature' option
  prefix                output prefix

optional arguments:
  -h, --help            show this help message and exit
  --sep SEP             separation
                        (default: 	)
  --dedimensions-method DEDIMENSIONS_METHOD
                        de-dimensions method
                        (default: PCA)
  --cluster-method CLUSTER_METHOD
                        cluster method
                        (default: MiniBatchKMeans)
  --assess-method ASSESS_METHOD
                        assess methods for best cluster number
                        (default: silhouette_score)
  --dimensions DIMENSIONS
                        reduce to n dimensions
                        (default: 3)
  --cluster-number CLUSTER_NUMBER
                        cluster number, if not specific it, it will be the best cluster number infered
                        (default: None)
  -r, --row-feature     row in the matrix represents feature
                        (default: True)
  --no-row-feature
  --annotation ANNOTATION
                        annotation file, sep should be ','
                        (default: None)
  --size SIZE           size column in annotation file
                        (default: None)
  --style STYLE         style column in annotation file
                        (default: None)
  -t TITLE, --title TITLE
                        figure title
                        (default: None)
  -f FIG, --fig FIG     png/pdf
                        (default: png)
  --version             show program's version number and exit
```



#### example

```bash
dedim.py tests/test.csv tests/test_result \
        --sep , --dimensions 2 \
        --no-row-feature --annotation tests/test_anno.csv \
        --style targets --title 'test PCA' \
        --dedimensions-method TSNE --fig png
```

![pca](tests/test_result_TSNE.png)

### fc_rename.py

```
usage: fc_rename.py [-h] [-s SAMPLE_TITLE] [-b BAM_TITLE] [-c COUNT_TITLE]
                    [--version]
                    featurecounts clinical prefix

featurecounts will use the bamfile name as the sample name. This script rename the featurecounts by the given table.

positional arguments:
  featurecounts         featurecounts table file
  clinical              clinical table file with header
  prefix                output prefix, there will be two outputs, one is count output (prefix_count.txt), and the other one is the rename featurecounts (prefix_fc.txt)

optional arguments:
  -h, --help            show this help message and exit
  -s SAMPLE_TITLE, --sample-title SAMPLE_TITLE
                        the column name of the sample name
                        (default: sample)
  -b BAM_TITLE, --bam-title BAM_TITLE
                        the column name of the bamfile name
                        (default: bam)
  -c COUNT_TITLE, --count-title COUNT_TITLE
                        the column name used as identity in count data
                        (default: Geneid)
  --version             show program's version number and exit
```
