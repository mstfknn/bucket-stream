# Bucket Stream

**Find interesting Amazon S3 Buckets by watching certificate transparency logs.**

This tool simply listens to various certificate transparency logs (via certstream) and attempts to find public S3 buckets from permutations of the certificates domain name.

> **Note:** This project has been updated and modernized for Python 3. The original project is no longer maintained by the original author, but has been updated to work with current dependencies and Python versions.

![Demo](https://i.imgur.com/ZFkIYhD.jpg)

**Be responsible**. I mainly created this tool to highlight the risks associated with public S3 buckets and to put a different spin on the usual dictionary based attacks. Some quick tips if you use S3 buckets:

1) Randomise your bucket names! There is no need to use `company-backup.s3.amazonaws.com`.
2) Set appropriate permissions and audit regularly. If possible create two buckets - one for your public assets and another for private data.
3) Be mindful about **your data**. What are suppliers, contractors and third parties doing with it? Where and how is it stored? These basic questions should be addressed in every info sec policy.
4) Try [Amazon Macie](https://aws.amazon.com/macie/) - it can automatically classify and secure sensitive data.

Thanks to my good friend David (@riskobscurity) for the idea.

## Installation

**Requirements:** Python 3.7+ (Python 3.8+ recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/eth0izzle/bucket-stream.git
   cd bucket-stream
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure (optional but recommended):
   Edit `config.yaml` and add your AWS credentials to avoid rate limiting:
   ```yaml
   aws_access_key: 'your-access-key'
   aws_secret: 'your-secret-key'
   ```

## Usage

### Basic Usage

Simply run:
```bash
python bucket-stream.py
```

If you provide AWS access and secret keys in `config.yaml`, Bucket Stream will attempt to access authenticated buckets and identify the bucket owner. **Unauthenticated users are severely rate limited (max 5 threads).**

### Command Line Options

```
usage: python bucket-stream.py

Find interesting Amazon S3 Buckets by watching certificate transparency logs.

options:
  -h, --help            Show this help message and exit
  --only-interesting    Only log 'interesting' buckets whose contents match
                        anything within keywords.txt (default: False)
  --skip-lets-encrypt   Skip certs (and thus listed domains) issued by Let's
                        Encrypt CA (default: False)
  -t, --threads         Number of threads to spawn. More threads = more power.
                        Limited to 5 threads if unauthenticated. (default: 20)
  --ignore-rate-limiting
                        If you ignore rate limits not all buckets will be
                        checked (default: False)
  -l, --log             Log found buckets to a file buckets.log (default: False)
  -s, --source SOURCE   Data source to check for bucket permutations. Uses
                        certificate transparency logs if not specified.
                        (default: None)
  -p, --permutations PERMUTATIONS
                        Path of file containing a list of permutations to try
                        (see permutations/ dir). (default: permutations/default.txt)
```

### Usage Examples

**Basic scan with CertStream:**
```bash
python bucket-stream.py
```

**Use extended permutations list (more comprehensive but slower):**
```bash
python bucket-stream.py -p permutations/extended.txt
```

**Scan specific domains from a file:**
```bash
python bucket-stream.py --source domains.txt --threads 10
```

**Only log interesting buckets (matching keywords.txt):**
```bash
python bucket-stream.py --only-interesting --log
```

This will only report buckets that contain files matching keywords in `keywords.txt` (e.g., password files, database dumps, configuration files, etc.).

**Skip Let's Encrypt certificates:**
```bash
python bucket-stream.py --skip-lets-encrypt
```

### Permutations

The tool uses permutation files to generate potential bucket names. Two files are provided:

- **`permutations/default.txt`** - ~30 common permutations (fast, recommended for most use cases)
- **`permutations/extended.txt`** - 1000+ permutations (comprehensive but slower)

You can create custom permutation files. Each line should contain `%s` where the domain name will be inserted, for example:
```
%s-backup
backup-%s
%s-data
data-%s
```

### Keywords Filtering

The `keywords.txt` file contains a list of sensitive keywords and file extensions used to identify "interesting" buckets when using the `--only-interesting` flag. The file includes:

- **Sensitive keywords**: password, secret, token, api-key, credentials, etc.
- **Database files**: .sql, .db, .dump, .backup, etc.
- **Configuration files**: .env, .pem, .key, config files, etc.
- **Source code**: .git, .svn, source code files, etc.
- **Archives**: .zip, .tar, .rar, compressed files, etc.
- **Documents**: .xls, .csv, .pdf, spreadsheets, etc.
- **Log files**: .log, access logs, error logs, etc.
- **Virtual machines**: .ova, .vmdk, disk images, etc.
- **And many more...**

The file contains **200+ keywords** organized by category. You can customize it by adding or removing keywords. Lines starting with `#` are treated as comments and ignored.

**Example keywords.txt:**
```
password
secret
.sql
.env
backup
```

## Updates & Improvements

This version includes the following updates:
- ✅ Updated to Python 3.7+ (removed Python 2 compatibility)
- ✅ Updated all dependencies to latest compatible versions
- ✅ Fixed CertStream connection issues
- ✅ Improved error handling and reconnection logic
- ✅ Enhanced default permutations list (~30 common patterns)
- ✅ Expanded keywords.txt file (200+ keywords across 15+ categories)
- ✅ Added comment support in keywords.txt (lines starting with # are ignored)
- ✅ Code modernization and cleanup

## F.A.Qs

- **Nothing appears to be happening**

   Patience! Sometimes certificate transparency logs can be quiet for a few minutes. The tool will show "Waiting for Certstream events..." and then "Connected to CertStream!" when connected. Ideally provide AWS secrets in `config.yaml` as this greatly speeds up the checking rate.

- **I'm getting rate limited**

   If you don't have AWS credentials, you're limited to 5 threads. Either:
   - Add AWS credentials to `config.yaml` (recommended)
   - Use `--ignore-rate-limiting` flag (may miss some buckets)
   - Reduce threads with `-t 3`

- **CertStream connection errors**

   The tool automatically retries on connection errors. If you see repeated errors, check your internet connection or try again later.

- **I found something highly confidential**

   **Report it** - please! You can usually figure out the owner from the bucket name or by doing some quick reconnaissance. Failing that contact Amazon's support teams.

## Troubleshooting

**Import errors:**
- Make sure you're using Python 3.7+
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use a virtual environment to avoid conflicts

**Connection issues:**
- CertStream may be temporarily unavailable
- Check your firewall/proxy settings
- The tool will automatically retry

**Rate limiting:**
- Add AWS credentials to `config.yaml` for better performance
- Without credentials, you're limited to 5 threads

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## License

MIT. See LICENSE
