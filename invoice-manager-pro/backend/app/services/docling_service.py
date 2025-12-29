try:
    from docling.document_converter import DocumentConverter
    from docling.datamodel.base_models import InputFormat
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False
    
from pathlib import Path
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DoclingService:
    """Service for processing PDFs using Docling library"""
    
    def __init__(self):
        if DOCLING_AVAILABLE:
            self.converter = DocumentConverter()
        else:
            self.converter = None
            logger.warning("Docling is not available. PDF processing will be disabled.")
    
    async def extract_pdf_data(self, file_path: str) -> Dict[str, Any]:
        """
        Extract structured data from PDF using Docling
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted data
        """
        try:
            if not self.converter:
                raise Exception("Docling library is not installed on this system.")
            
            # Convert PDF to DoclingDocument
            result = self.converter.convert(file_path)
            
            # Extract text content
            text_content = result.document.export_to_markdown()
            
            # Extract tables if present
            tables = []
            for table in result.document.tables:
                table_data = {
                    "data": table.export_to_dataframe().to_dict('records'),
                    "caption": getattr(table, 'caption', None)
                }
                tables.append(table_data)
            
            # Build structured output
            extracted_data = {
                "text": text_content,
                "tables": tables,
                "metadata": {
                    "num_pages": result.document.num_pages,
                    "title": getattr(result.document, 'title', None),
                }
            }
            
            logger.info(f"Successfully extracted data from PDF: {file_path}")
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error extracting PDF data: {str(e)}")
            raise
    
    async def extract_price_list(self, file_path: str) -> Dict[str, Any]:
        """
        Extract price list data from supplier PDF
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing price list items
        """
        try:
            extracted_data = await self.extract_pdf_data(file_path)
            
            # Process tables to extract price information
            price_items = []
            
            for table in extracted_data.get("tables", []):
                for row in table.get("data", []):
                    # Attempt to identify price columns
                    # This is a simplified version - you may need to customize
                    # based on your specific PDF format
                    item = self._parse_price_row(row)
                    if item:
                        price_items.append(item)
            
            return {
                "items": price_items,
                "raw_text": extracted_data.get("text", ""),
                "total_items": len(price_items)
            }
            
        except Exception as e:
            logger.error(f"Error extracting price list: {str(e)}")
            raise
    
    def _parse_price_row(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse a table row to extract price information
        
        Args:
            row: Dictionary representing a table row
            
        Returns:
            Parsed item dictionary or None if not valid
        """
        # This is a template - customize based on your PDF structure
        try:
            item = {}
            
            # Common field mappings (adjust as needed)
            field_mappings = {
                'item': ['item', 'producto', 'product', 'descripcion', 'description'],
                'sku': ['sku', 'codigo', 'code', 'part_number'],
                'price': ['price', 'precio', 'unit_price', 'precio_unitario'],
                'quantity': ['quantity', 'cantidad', 'qty'],
                'unit': ['unit', 'unidad', 'uom']
            }
            
            for field, possible_keys in field_mappings.items():
                for key in possible_keys:
                    if key.lower() in [k.lower() for k in row.keys()]:
                        actual_key = next(k for k in row.keys() if k.lower() == key.lower())
                        item[field] = row[actual_key]
                        break
            
            # Only return if we have at least item name and price
            if 'item' in item and 'price' in item:
                return item
            
            return None
            
        except Exception as e:
            logger.warning(f"Error parsing price row: {str(e)}")
            return None
    
    async def extract_invoice_data(self, file_path: str) -> Dict[str, Any]:
        """
        Extract invoice data from PDF
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing invoice information
        """
        try:
            extracted_data = await self.extract_pdf_data(file_path)
            
            # Extract invoice-specific information
            # This is a template - customize based on your invoice format
            invoice_data = {
                "text": extracted_data.get("text", ""),
                "tables": extracted_data.get("tables", []),
                "metadata": extracted_data.get("metadata", {})
            }
            
            return invoice_data
            
        except Exception as e:
            logger.error(f"Error extracting invoice data: {str(e)}")
            raise


# Singleton instance
docling_service = DoclingService()
