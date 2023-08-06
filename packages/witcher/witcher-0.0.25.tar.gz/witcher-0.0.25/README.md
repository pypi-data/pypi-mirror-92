# witcher
Witcher is an automated, driverless tool to build an error-free machine learning application.


Witcher is an automated AI application designed to speed up the data processing phases.
The current witcher has :

<UL>

<li><B>Recommender:</B> will provide you with a comprehensive product recommendation using product popularity, product similarity and user similarity models.</li>


<li><B>StockMarket :</B> Will read the stock information from Yahoo API and analysis the Stock prices using ARIMA Time series</li>


<li><B>FileChooser :</B> Automated FileChooser function, Filechooser will read your data regardless it format and will provides you a Datafram. Currently witcher can read csv,xls,xlsx,sas,and images automaticaly </li>


<li><B>ImageToCartoon :</B> A fun project will read your images and do some processing such as image blurred, edges extraction, image to cartoon,...</li>
</UL>


 
Magical data processing, predictive, and deep learning models will be joining witchers functions very soon :)

I hope you will enjoy using the witcher library


Thank you. 


Babak.EA



How to run : 

<b> using Jupyter notbook </b> 

<UL>

<li><B>import wirtcher </B></li>
<li><B>from witcher import Recommender</B></li>
<li><B>from witcher import StockMarket</B></li>
<li><B>from witcher import FileChooser</B></li>
<li><B>from witcher import ImageToCartoon</B></li>
</UL>


from witcher import FileChooser

        FileChooser.Filechooser ==>
		
        will read the file and will returen the filename, filepath, and dataframe for
        CSV, XLS,XLSX, SAS, and Images
		

        Reprort=witcher.FileChooser.filechoose()
		
        Report
		

        report.files == > file path
		
        report.df ==> dataframe
		

    from witcher import FileChooser, ImageToCartoon
	
        img=FileChooser.Filechooser()
		
        img
		

        image=img.df or
		
        image=ImageToCartoon.Img_Reader(img.files[0]) # read image and return numpy vector
		

        ImageToCartoon.ImageShow(image) ### Show the image
		
        Image_D=IMG_D=ImageToCartoon.Decolorization(image)
		
        Blurred=Blurred(image)
		
        edges=ImageToCartoon.Edgedetection(image)
		
        Bluured=ImageToCartoon.Blurred(image)
		
        Cartoon=Cartoon(bluured=Blurred,mask=edges)
		
        or
		
        Cartoon=Cartoon(bluured=Blurred,decolor=Image_D,mask=edges)
		


    from witcher import StockMarket
	
        select your stock and starting date to end date
		
        df=StockMarket.Stock_Reader(stock=["AC.TO"],Period="1D",Start_date="2010-01-01",End_date="Today")
		
        df=StockMarket.Dataset_Spliter(df,col="Close",split=.1,Forecasting=True)
		
        select the column you want to analysis and pass it to the finction 






source code : github
https://github.com/BabakEA/witcher

YouTube:https://www.youtube.com/channel/UCBqqRv8vWV3NZFF2tQV4e-w

PyPi : 
pip install witcher 
