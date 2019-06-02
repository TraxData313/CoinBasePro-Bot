<p><em>Disclaimer:</em></p>
<blockquote>
<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>
</blockquote>


# Information:
- Python 2.7 compatible
- File: current_price.py - when run it will display the current prices for BTC, LTC and ETH
- File: stat_create.py - will gather the desired amount of price statistics. Once done, it will create the price statistic files and will maintain them
- File: stat_maintain.py - when run will load already collected price statistics and will maintain them
- For troubleshooting use the error logs: "CurrentPrice.error.log" and "Stat.error.log"


# Usage:
- Install the cbpro library with command:<br>
<i>pip intall cbpro</i>
- Run the price monitor: 
- - Download file "current_price.py", open command prompt and run the script:
- - <i>python current_price.py</i>
- Run the statistics collector:
- - Download file "statistics_maintain.py", open command prompt and run the script:
- - <i>statistics_maintain.py</i>
- - The stat maintan script will take date from the monitor every one minute and append it to the stat files
- - TIP: download the stats for the whole year from, for example, http://www.cryptodatadownload.com/data/northamerican/, then run the maintan script, which will keep the data updated at all times. The downloaded data is most likely in reverse order (newest on top), to get it in the right order, use the reverser script ot it.

... Under construction. I still need to remove personal data from the files and then add them. If you need help with something specific in the mean time (like: how to place or cancel order, how to check ballance...), please feel free to contact me @ antongeorgiev313@gmail.com
