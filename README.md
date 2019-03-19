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
- - Download file "stat_create.py", open command prompt and run the script:
- - Edit the file and set the two parameters* inside
- - <i>python stat_create.py</i>
- - Once the statistics have been collected, the file will auto-start keeping it fresh (maintaining it). 
- - Download file "stat_maintain.py", edit it to make sure the parameters* match the ones in "stat_create.py"
- - If the "stat_create.py" has stopped for some reason (for ex after server reboot), run the "stat_maintain.py" to load the current statistics
- - *parameters:
- - - stat_total_time determines how long the statistics will be in seconds. For example, setting it to 604800 will collect 7 days worth of statistics
- - - stat_refresh_rate determines the refresh rate in seconds

... Under construction. Still adding files and their descriptions.
